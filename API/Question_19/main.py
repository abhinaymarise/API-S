from Question_19.src.email_reader import headers
from Question_19.src.util import connection

df=headers()

df["Attachments"] = df["Attachments"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)


try:
    engine=connection()
    df.to_sql("Mail_Data",con=engine,if_exists='replace',index=False)
    print("Data sent into SQL Server!")
except Exception as e:
    print("Not sent!",e)
