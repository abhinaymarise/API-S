from Question_19.src.util import s3_client
import re

def slice_name(name):
    name_only = re.sub(r'\s*<[^>]+>', '', name).strip() 
    return re.sub(r'[^\w\-]', '_', name_only) 

# ================ For uploading into s3 bucket ===================

def upload_into_s3(bucket_name, sender_email, attachments, msg_id):

    s3 = s3_client()
    sender_folder = slice_name(sender_email)

    for index, attachment in enumerate(attachments,start=1):
        filename = attachment["filename"]
        file_data = attachment["data"]

        s3_key = f"gmailextract/attachments/{msg_id}/{sender_folder}/{index}_{filename}"

        try:
            s3.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=file_data
            )
            print("Successfully Uploaded")
        except Exception as e:
            print(f"Failed to upload {filename}: {e}")
