# RTF-Extractor

RTF-Extractor is a Python package that takes an RTF file as input, converts it to plain text, and performs various text mining operations to extract important features from the document and seperate diffrent articles. 

---
## Features
The following are some of the key features of RTF-Extractor:

* RTF to text conversion: The package can convert RTF files to plain text, preserving formatting where possible.

* Text cleaning: The package includes a set of functions for cleaning the text, removing unwanted characters and formatting.

* Article separation: The package can separate different articles within a single RTF file.

* Feature extraction: The package includes a set of functions for extracting important features from the text, such as title, publication date, organizayion.

* Save articles: Save seperated articles with name format using the extracted features.

## Requirements
      pip install -r requirements.txt
      
---
## Usage
To use RTF-Extractor, users can clone the repository and install the required dependencies. Then, they can import the relevant functions from the package and customize them as needed. Here's an example workflow:

**run the code on one file**

      file_path = "files/articles.rtf"
      folder_path = "/".join(file_path.split("/")[:-1])
      extractor = RTFExtractor(file_path)
      extractor.transform(output_folder1 = os.path.join(folder_path, "Folder A"), output_folder2 =  os.path.join(folder_path, "Folder B"))


**run all the files inside a folder**
      folder_path = "files"
      rtf_files = glob.glob(os.path.join(folder_path, "*.rtf"))

      print(f"We have {len(rtf_files)} rtf files")
      for rtf_file in tqdm(rtf_files):
          print("\n", rtf_file)
          extractor = RTFExtractor(rtf_file)
          extractor.transform(output_folder1 = os.path.join(folder_path, "Folder A"), output_folder2 =  os.path.join(folder_path, "Folder B"))
