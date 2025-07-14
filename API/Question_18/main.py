from Question_18.src.util import sharepoint_conn,connection
from Question_18.src.create_db import create_database

dfs=sharepoint_conn()


create_database("SharePoint")

try:
    engine=connection()
    for df in dfs:
        df.to_sql("SP_Data",con=engine,if_exists='replace',index=False)
        print("Data sent into SQL Server!")
except Exception as e:
    print("Not sent!",e)
