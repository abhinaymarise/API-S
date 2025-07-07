from Question_14.src.Config.config import ssms_db_config,ssms_url
import pyodbc
from sqlalchemy import create_engine

def ssms_connection():
    db=ssms_db_config
    conn=(
        f"Driver={db['driver']};"
        f"Server={db['server']};"
        f"UID={db['username']};"
        f"PWD={db['password']};"
        f"Database={db['database']}"
    )
    return pyodbc.connect(conn,autocommit=True)

def connect():
    engine=create_engine(ssms_url)
    return engine