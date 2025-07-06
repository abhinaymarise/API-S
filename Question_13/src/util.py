from Question_13.src.Config.config import ssms_db_config,ssms_url
import pyodbc
from sqlmodel import create_engine,SQLModel,Session
from Question_13.src.models import Student

#========== Establishing a Database Connection =================

def ssms_connection():
    db=ssms_db_config
    conn=(
        f"Driver={db['driver']};"
        f"Server={db['server']};"
        f"UID={db['username']};"
        f"PWD={db['password']};"
        f"Database={db['database']};"
    )
    return pyodbc.connect(conn,autocommit=True)

#====== Creating a Table using the SQLMODEL through the engine ==================

def connect():
    engine=create_engine(ssms_url,echo=True)
    SQLModel.metadata.create_all(engine)
    return engine

#========== Session Function is written because it allows the fastapi endpoints to connect/talk to the database ===

def get_session():
    engine=connect()
    return Session(engine)