from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.files.file import File
from io import BytesIO
import pandas as pd
from Question_18.src.Config.config import SHAREPOINT_SITE_URL,USERNAME,PASSWORD,LIBRARY
import pyodbc

def sharepoint_conn():
        
        dfs=[]
        # ================ Connection to the SharePoint =========================

        auth=ClientContext(SHAREPOINT_SITE_URL).with_credentials(UserCredential(USERNAME,PASSWORD))

        # ============= Set Folder path to read files from =====================

        folder=f"/sites/kasmo-training/Abhinay"
        folder_obj=auth.web.get_folder_by_server_relative_url(folder)

        # ================== Get all the files from the Folder ===================

        files=folder_obj.files
        auth.load(files)
        auth.execute_query()

        # ======================== Loop over each file ============================

        for file in files:
                    
                file_name=file.properties['Name']
                file_url=file.properties["ServerRelativeUrl"]
                print(f"\n Reading: {file_name}")       
                response=File.open_binary(auth,file_url)
                file_stream=BytesIO(response.content)

                if file_name.endswith(".xlsx"):
                        df=pd.read_excel(file_stream)
                        dfs.append(df)
                        print(df.head())

        return dfs



# ============== SSMS Connection ========================

from Question_18.src.Config.config import ssms_db_config,ssms_url
from sqlalchemy import create_engine

def ssms_connection():
    db = ssms_db_config
    conn = (
        f"Driver={db['driver']};"
        f"Server={db['server']};"
        f"UID={db['username']};"
        f"PWD={db['password']};"
        f"Database={db['database']}"
    )
    return pyodbc.connect(conn, autocommit=True)


def connection():
    engine=create_engine(ssms_url)
    return engine



