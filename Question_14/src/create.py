from Question_14.src.util import ssms_connection

def create_database(db_name):
    con=ssms_connection()
    cursor=con.cursor()

    try:
        cursor.execute("Select name from sys.databases where name=?",db_name)
        result=cursor.fetchone()

        if result:
            print(f"Database {db_name} already exists!")
        else:
            cursor.execute(f"Create Database {db_name}")
            print(f"Database {db_name} created successfully")
    except Exception as e:
        print("Work more on Database Creation",e)
    finally:
        cursor.commit()
        con.commit()
    
create_database("X_Data")