import os
import pandas as pd
from Question_15.src.extract_fields import extract_email,extract_name,extract_phone,extract_skills,extract_experience_summary,extract_education_summary
from Question_15.src.create import create_database
from Question_15.src.util import connection
import sys

Base_Dir=os.path.dirname(__file__)
Resume_Dir=os.path.join(Base_Dir,"Extracted_Resume")

def filter_resume():
    extracted_data=[]

    for file in os.listdir(Resume_Dir):

        if file.endswith(".txt"):
            file_path=os.path.join(Resume_Dir,file)
            with open(file_path)as f:
                text=f.read()

            email=extract_email(text)
            name=extract_name(text,email)
            phone=extract_phone(text)
            skills=extract_skills(text)
            education=extract_education_summary(text)
            experience=extract_experience_summary(text)

            extracted_data.append({
                 'Name':name,
                 'Email':email,
                 'Phone':phone,
                 'Skills':skills,
                 'Education_Summary':education,
                 'Experience_Summary':experience
             })

    df=pd.DataFrame(extracted_data)
    return df

# ========== Data sent into Database ===================

df=filter_resume()

try:
    engine=connection()
    df.to_sql("Resume_Data",con=engine,if_exists='replace',index=False)
    print("Data Sent into Database")
except Exception as e:
    print("Too close, Cross check the code again",e)

if __name__=='__main__':
    if len(sys.argv)<2:
        sys.exit(1)
    functions=sys.argv[1]

    if functions=="filter_resume":
        df=filter_resume()
        print("Extracted Resume Data:\n")
        print(df["Skills"])
    elif functions=="create_database":
        create_database("Unstructured_Data_Handling")
    else:
        print("Function name doesnt exists or given wrong!")