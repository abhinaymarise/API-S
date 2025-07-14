from Question_15.src.parse import parse_all_pdfs_from_s3 #,saved_parsed_data

# ======== Access to the S3 BUCKET Folders ===============

BUCKET_NAME="unstructpdfanalyzer"
Folder_Resume="resume/"
Folder_Transform="transform/"
Folder_Archive="archive/"

 
parse_resume=parse_all_pdfs_from_s3(BUCKET_NAME,Folder_Resume,Folder_Transform,Folder_Archive)

for key, text in parse_resume.items():
    print(f"\n======== {key} =========\n{text[:500]}........\n")

# saved_parsed_data(parse_resume,"Extracted_Resume")

