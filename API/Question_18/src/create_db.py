from Question_18.src.util import ssms_connection

def create_database(db_name):
    conn=ssms_connection()
    cursor=conn.cursor()

    try:
        cursor.execute("Select name from sys.databases where name=?",db_name)
        result=cursor.fetchone()

        if result:
            print(f"Database {db_name} already exists!")
        else:
            cursor.execute(f"Create Database {db_name}")
            print(f"{db_name} created successfully!")

    except Exception as e:
         print("Work more on Db creation",e)




