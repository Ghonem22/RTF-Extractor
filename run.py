from rtf_extractor.rtf_extractor import *
import glob
import os
from tqdm import tqdm



# process the code on one file
file_path = "files/articles.rtf"
folder_path = "/".join(file_path.split("/")[:-1])
extractor = RTFExtractor(file_path)
extractor.transform(output_folder1 = os.path.join(folder_path, "Folder A"), output_folder2 =  os.path.join(folder_path, "Folder B"))



# process all the files inside a folder
folder_path = "files"
rtf_files = glob.glob(os.path.join(folder_path, "*.rtf"))

print(f"We have {len(rtf_files)} rtf files")
for rtf_file in tqdm(rtf_files):
    print("\n", rtf_file)
    extractor = RTFExtractor(rtf_file)
    extractor.transform(output_folder1 = os.path.join(folder_path, "Folder A"), output_folder2 =  os.path.join(folder_path, "Folder B"))
