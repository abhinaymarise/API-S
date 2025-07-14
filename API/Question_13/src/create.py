from Question_13.src.util import ssms_connection

def db_creation(db_name):
    conn=ssms_connection()
    cursor=conn.cursor()

    try:
        cursor.execute('Select name from sys.databases where name = ?',db_name)
        result=cursor.fetchone()
        if result:
            print(f'Database {db_name} exists.')
        else:
            cursor.execute(f"Create database {db_name}")
            print(f"Database {db_name} created successfully!")
    except Exception as e:
        print("Work more on DB Creation",e)
    finally:
        cursor.commit()
        conn.commit()
