# ============== AWS Connection =====================

from dotenv import load_dotenv
import os
import boto3

load_dotenv()

def get_s3_client():
    return boto3.client("s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION"))


# ============== SSMS Connection ========================

from Question_15.src.Config.config import ssms_db_config,ssms_url
import pyodbc
from sqlalchemy import create_engine

def ssms_connection():
    db=ssms_db_config
    conn=(
        f"Driver={db['Driver']};"
        f"Server={db['Server']};"
        f"UID={db['username']};"
        f"PWD={db['password']};"
        f"Database={db['database']};"
    )
    return pyodbc.connect(conn,autocommit=True)

def connection():
    engine=create_engine(ssms_url)
    return engine

