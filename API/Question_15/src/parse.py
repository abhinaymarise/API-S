from Question_15.src.util import get_s3_client
from io import BytesIO
from pdfminer.high_level import extract_text
import os

def parse_all_pdfs_from_s3(bucket:str,prefix:str,destination,archive):
    s3=get_s3_client()
    res = s3.list_objects_v2(Bucket=bucket,Prefix=prefix)

    results={}

    for obj in res.get("Contents",[]):
        key=obj["Key"]
        if key.lower().endswith(".pdf"):
            print(f"Parsing: {key}")

            try:
                pdf_stream=s3.get_object(Bucket=bucket,Key=key)["Body"].read()
                text=extract_text(BytesIO(pdf_stream))
                results[key]=text
                print(f"Done with {key} parsing!")

# ============== Upload the file into transform ============

                file_name=os.path.basename(key).replace(".pdf",".txt")
                text_key=destination+file_name

                s3.put_object(
                    Bucket=bucket,
                    Key=text_key,
                    Body=text.encode("utf-8"),
                    ContentType="text/plain"
                )
                print("Successfully Uploaded!!")

# ================= Copy the pdf into archive =================

                archive_key=archive+os.path.basename(key)
                s3.copy_object(
                    Bucket=bucket,
                    Key=archive_key,
                    CopySource={"Bucket":bucket,"Key":key}
                )

# ========= Delete the pdf from source ===============

                s3.delete_object(
                        Bucket=bucket,
                        Key=key
                        )
                print("Successfully Erased from Source!")
            except Exception as e:
                print(f"Failed to parse {key}",e)
    
    return results


# =========== Save the parsed resumes in local machine ===============

# from pathlib import Path 

# def saved_parsed_data(parsed_data,folder_name):
#     ouput_folder=Path(folder_name)
#     ouput_folder.mkdir(exist_ok=True)

#     for s3_key, text_content in parsed_data.items():
#         pdf_filename=Path(s3_key).name
#         text_format=pdf_filename.replace(".pdf",".txt")
#         full_text_path=text_format

#         with Path(full_text_path).open(mode="w",encoding="utf-8") as file:
#             file.write(text_content)   
          

