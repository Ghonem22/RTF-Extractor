import os
import re
from datetime import datetime
from striprtf.striprtf import rtf_to_text


class RTFExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

        # Read the file contents into memory
        with open(file_path, mode="r", errors="ignore", encoding="utf-8") as f:
            self.file_contents = f.read()

    def clean_data(self, batch_len=5000):
        """
        Cleans the raw RTF file contents and returns the cleaned text.

        Args:
            batch_len (int): The length of each batch of text to clean (default 5000).

        Returns:
            str: The cleaned text.
        """
        result = ''

        for i in range(len(self.file_contents) // batch_len):
            result += rtf_to_text(self.file_contents[i * batch_len: (i + 1) * batch_len])

        return result

    def separate_articles(self):
        """
        Separates the text into different articles based on some criteria.

        Returns:
            List[str]: A list of the separated articles.
        """
        sections = self.clean_data().split("LINKS\nFULL TEXT")
        headers = []
        contents = []
        tables = []
        full_contents = []
        for i, section in enumerate(sections):

            if i == 0:
                header = section
                headers.append(header)

            elif i == len(sections) - 1:
                last_content = section
                full_contents.append(last_content)
                main_content, table = self.separate_content_and_table(last_content)

                contents.append(main_content)
                tables.append(table)

            else:
                last_content, header = self.get_data(section)
                full_contents.append(last_content)
                main_content, table = self.separate_content_and_table(last_content)

                headers.append(header)
                contents.append(main_content)
                tables.append(table)

        return contents, tables, headers

    def separate_content_and_table(self, content):
        """
        Separates the main content from the table below it.

        Args:
            content (str): The content to separate.

        Returns:
            Tuple[str, str]: The main content and the table as separate strings.
        """
        if "\nDETAILS\n" in content:
            splited_content = content.split("\nDETAILS\n")
            main_content = splited_content[0]
            table = splited_content[1]

        else:
            splited_content = content.split("\n")
            i = self.get_corrupted_section(splited_content)
            if i != -1:
                main_content = "\n".join(splited_content[0:i])
                table = "\n".join(splited_content[i + 1:])
            else:
                return content, ""

        return main_content, table

    def get_data(self, section):
        """
        Extracts the header and content from a section of the text.

        Args:
            section (str): The section of the text to extract from.

        Returns:
            Tuple[str, str]: The header and content as separate strings.
        """
        content = header = ''
        # take section from text and return content, next_title, next_abstract
        parts = section.split("\n |\n")
        parts = [part for part in parts if part not in ['\n\n', '', None]]

        last_content = parts[0]
        header = "\n |\n".join(parts[1:])

        return last_content, header

    def get_corrupted_section(self, splitted_text, thresh=1500):
        """
        Finds the index of a corrupted section of text.

        Args:
            splitted_text (List[str]): The text to search for the corrupted section.
            thresh (int): The threshold length to consider a section as corrupted (default 1500).

        Returns:
            int: The index of the corrupted section, or -1 if no corrupted section is found.
        """
        # corrupted section is very long section > thresh
        for i, c in enumerate(splitted_text):
            if len(c) > thresh:
                return i

        return -1

    def extract_meta_data(self, table):
        """
        Extracts the metadata from a table.

        Args:
            table (str): The table to extract metadata from.

        Returns:
            Tuple[str, str, str]: The source, firm, and publication date as separate strings.
        """
        table_lines = table.split("\n")
        source = firm = pub_dat = ''
        for line in table_lines:
            if "publication title" in line.lower():
                source = line.split(";")[0].split("|")[-1].split(",")[0].strip()
            elif "company / organization" in line.lower():
                firm = line.split("Name: ")[-1].split(";")[0].strip()
            elif "publication date" in line.lower():
                matches = re.findall(r"[A-Z][a-z]{2}\s\d{1,2},\s\d{4}", line)
                if matches:
                    pub_dat = matches[0]

            if source and firm and pub_dat:
                return source, firm, pub_dat

        return source, firm, pub_dat

    def convert_date_format(self, date_string, input_format='%b %d, %Y', output_format='%Y_%m_%d'):
        """
        Converts a date string from one format to another.

        Args:
            date_string (str): The date string to convert.
            input_format (str): The format of the input date string (default '%b %d,Here's the continuation of the previous code:
        """
        date = datetime.strptime(date_string, input_format)
        return date.strftime(output_format)

    def get_file_name(self, content, table):
        """
        Generates the file name based on the metadata.

        Args:
            content (str): The content of the article.
            table (str): The table containing the metadata.

        Returns:
            str: The file name.
        """
        result = True
        source, firm, pub_dat = self.extract_meta_data(table)
        if not (source and firm and pub_dat):
            content_source, content_firm, content_pub_dat = self.extract_meta_data(content)
            source, firm, pub_dat = source or content_source, firm or content_firm, pub_dat or content_pub_dat

        if pub_dat:
            try:
                pub_dat = self.convert_date_format(pub_dat)
            except:
                result = False

        if not result:
            pub_dat = "error_date"

        if not source:
            source = "error_source"
            result = False
        if not firm:
            firm = "error_firm"
            result = False

        return f"{source}_{firm}_{pub_dat}", result

    def transform(self, output_folder):
        """
        Organizes the articles into separate files and saves them to disk.

        Args:
            output_folder (str): The folder to save the files to.
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        contents, tables, headers = self.separate_articles()

        # Keep track of how many articles were saved for each publication date
        dates = {}
        idx = 1
        error_idx = 1

        # Loop through each article and save it to disk
        for i, (header, content, table) in enumerate(zip(headers, contents, tables)):
            # Merge the file
            article = header + "\nLINKS\nFULL TEXT\n" + content

            # Get the file name
            file_name, result = self.get_file_name(content, table)

            # Add a number to the end of the file name if there are multiple articles with the same name
            if result:
                if not dates.get(file_name):
                    dates[file_name] = 0

                dates[file_name] += 1
                file_name = f"{file_name}_{dates[file_name]}"
            else:
                file_name = f"error_{error_idx}"
                error_idx += 1

            # Save the file to disk
            file_path = os.path.join(output_folder, file_name + ".txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(article)
