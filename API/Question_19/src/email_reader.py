from Question_19.src.gmail_auth import get_service
from bs4 import BeautifulSoup
import base64,imgkit
from io import BytesIO
from Question_19.src.load_into_s3 import upload_into_s3,slice_name
from Question_19.src.util import s3_client
import pandas as pd

service=get_service()

# ====== The first 10 gmails ID retrieval =================

response=service.users().messages().list(userId="me",labelIds=["INBOX"],maxResults=12,q="is:unread").execute()
msg_ids=[msg["id"] for msg in response.get("messages",[])]
print("Fetched", len(msg_ids), "message IDs")

# ========== Fetches each unread mesaage in full format (payload) for each msg id =================

def headers():
    email_count=0
    all_emails=[]

    def is_valid_html(content):
        try:
            soup=BeautifulSoup(content,'html.parser')
            return bool(soup.find())
        except:
            return False
    for msg_id in msg_ids:
        message=service.users().messages().get(userId="me",id=msg_id,format="full").execute()
    
    # ======================= Extract the headers from the email =============================
    
        headers=message["payload"]["headers"]

        def get_headers(headers,name):
            for h in headers:
                if h["name"]==name:
                    return h["value"]
            return None
        
        # ================= For Body <Plain/Text> Itself =============================

        def extract_text_from_body(payload):
            text=[]
            def recurse(parts):
                for part in parts:
                        if part.get("mimeType")=='text/plain':
                            data=part.get("body",{}).get("data")
                            if data:
                                decoded = base64.urlsafe_b64decode(data).decode('utf-8',errors='replace')
                                text.append(decoded)
                        elif part.get("parts"):
                            recurse(part["parts"])

            if "parts" in payload:
                recurse(payload["parts"])
            elif payload.get("mimeType")=='text/plain':
                data=payload.get("body",{}).get("data")
                if data:
                    decode = base64.urlsafe_b64decode(data).decode("utf-8",errors='replace')
                    text.append(decode)
            
            return "\n".join(text) if text else None
        
        # ======================== For Body <Html/Text> Itself ========================

        def extract_html_text_from_body(payload):
            if "parts" in payload:
                for part in payload["parts"]:
                    if part.get("mimeType")=='text/html':
                        data=part["body"].get("data")

                        if data:
                            decoded=base64.urlsafe_b64decode(data).decode("utf-8",errors='replace')
                            return decoded

            elif payload.get("mimeType")=="text/html":
                data=payload["body"].get("data")

                if data:
                    decoded=base64.urlsafe_b64decode(data).decode("utf-8",errors="replace")
                    return decoded
                    
            return  None
        
    # ===================== Attachments ===============================================

        def extract_attachments(payload,message_id,service):
            attachments=[]

            def recurse(parts):
                for part in parts:
                    if part.get("parts"):
                        recurse(part["parts"])
                    else:
                        filename=part.get("filename")
                        body=part.get("body")
                        attachment_id=body.get("attachmentId")

                        if not filename:
                            continue

                        if attachment_id:
                            attachment=service.users().messages().attachments().get(userId="me",messageId=message_id,id=attachment_id).execute()
                            data=base64.urlsafe_b64decode(attachment["data"])
                        else:
                            try:
                                data=base64.urlsafe_b64decode(body.get("data",""))
                            except Exception as e:
                                print("Base 64 code error")

                        attachments.append({
                            "filename":filename,
                            "mimeType":part.get("mimeType"),
                            "data": data
                        })
                    
            if "parts" in payload:
                recurse(payload["parts"])

            return attachments


        payload=message.get("payload",{})

    # ========================= Function Calls =====================================

        sender=get_headers(headers,"From")
        to=get_headers(headers,"To")
        cc=get_headers(headers,"Cc")
        subject=get_headers(headers,"Subject")
        date_str=get_headers(headers,"Date")
        body=extract_text_from_body(payload)
        body_html_text=extract_html_text_from_body(payload)

    # =========== Extract the multiple images from the webpage ======================

        def extract_external_images(html_text):
            soup=BeautifulSoup(html_text,"html.parser")
            image_urls=[]
            for img_tag in soup.find_all("img"):
                src=img_tag.get("src")
                if src and src.startswith("http"):
                    image_urls.append(src)
            return image_urls
        
        
        external_image_urls=extract_external_images(body_html_text) if body_html_text else None

        if external_image_urls:
            for url in external_image_urls:
                print(url)
        else:
            print("No external Image present!")

    # ============== Print the headers and body ========================================
    
        print("-"*100)
        print("From :",sender)
        print("To: ",to)
        print("Cc: ",cc)
        print("Subject: ",subject)
        print("Date: ",date_str)
        print("Body: ",body)
        print("Html_Body_Text: ",body_html_text[:100] if body_html_text else None)


    # ================== Combining multiple images extracted  ===============================

        html_img_url=None
        if body_html_text and is_valid_html(body_html_text):
            external_image_urls=extract_external_images(body_html_text)

        # ================ Sending directly into s3 bucket ===================================

            if external_image_urls:
                email_count+=1

                try:
                    config = imgkit.config(wkhtmltoimage=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe")
                    image_binary=imgkit.from_string(body_html_text,False,config=config)
                    print("HTML to Image converted")

                    s3_client().put_object(Bucket="gmailextract",Key=f"html_images/{msg_id}.jpg",Body=BytesIO(image_binary),ContentType="image/jpeg")
                    print("Html Image sent into s3 bucket")
                    html_img_url=f"https://gmailextract.s3.ap-south-1.amazonaws.com/html_images/{msg_id}.jpg"
                except Exception as e:
                    print("not converted",e)

        attachments=extract_attachments(payload,msg_id,service)
        attachment_urls=[]
        if attachments:
            print(f"{len(attachments)} attachements found")
            for attach in attachments:
                print("Attachment: ",attach["filename"])
                print("MimeType: ",attach["mimeType"])

            # =========== Attachments Uploaded into s3 bucket ============

            upload_into_s3("gmailextract",sender,attachments,msg_id)

            sender_folder=slice_name(sender)
            for i, attach in enumerate(attachments,1):
                filename=attach["filename"]
                attachment_urls.append(f"https://gmailextract.s3.ap-south-1.amazonaws.com/attachments/{msg_id}/{sender_folder}/{i}_{filename}")
        
        # ================= It adds multiple attachments into each row ==================

        if attachment_urls:
            for url in attachment_urls:
                email_record={
                    "From":sender,
                    "To":to,
                    "Cc":cc,
                    "Date":date_str,
                    "Subject":subject,
                    "Plain Text":body if body else None,
                    "HTML Image":html_img_url if html_img_url else None,
                    "Attachments":url
                }
                all_emails.append(email_record)
        else:
            email_record={
                    "From":sender,
                    "To":to,
                    "Cc":cc,
                    "Date":date_str,
                    "Subject":subject,
                    "Plain Text":body if body else None,
                    "HTML Image":html_img_url if html_img_url else None,
                    "Attachments":None
                }

            all_emails.append(email_record)

        # ============== Marking Unread Emails as read emails =============

        try:
            service.users().messages().modify(userId="me",id=msg_id,body={"removeLabelIds":["UNREAD"]}).execute()
            print('Emails are markded as read')
        except Exception as e:
            print(f"Could not make it read!")

 # ======== Converting into dataframe ==============

    df=pd.DataFrame(all_emails)
    #print(df)
    return df
        


    