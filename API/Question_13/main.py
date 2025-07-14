from Question_13.src.util import ssms_connection,connect
from Question_13.src.create import db_creation
import sys

if __name__=="__main__":
    if(len(sys.argv)<2):
        sys.exit(1)
    function=sys.argv[1]

    if function =='ssms_connection':
        ssms_connection()
    elif function =='connect':
        connect()
    elif function == 'db_creation':
        db_creation("API_Data")

# =============== API Creation =============================

# =============== POST Method =============================

from Question_13.src.util import get_session
from Question_13.src.models import Student,StudentResponse
from sqlmodel import select
from fastapi import FastAPI, HTTPException

app=FastAPI()

@app.post("/create-student/{student_id}")
def create_student(student_id:int, student:Student):
    session=get_session()

    statement=select(Student).where(Student.id==student_id)
    result=session.exec(statement)
    fetch=result.first()

    if fetch:
        raise HTTPException(status_code=400,detail="Error: Student Already Exists")
    
    student.id=student_id
    session.add(student)
    session.commit()
    session.refresh(student)

    return student

#============= GET Method ========================

@app.get("/get-student/{student_id}",response_model=StudentResponse)
def get_student(student_id:int):
    session=get_session()
    student=session.get(Student,student_id)

    if student:
        return student
    raise HTTPException(status_code=404,detail="Student Not Found")


# ============= PUT Method ==========================
@app.put("/update-student/{student_id}")
def update_student(student_id:int, student:Student):
    session=get_session()

    statement=select(Student).where(Student.id==student_id)
    query=session.exec(statement)
    db_student=query.first()

    if db_student:
        if student.Name is not None:
            db_student.Name=student.Name
        if student.Age is not None:
            db_student.Age=student.Age
        if student.Email is not None:
            db_student.Email=student.Email
        if student.Country is not None:
            db_student.Country=student.Country

        session.commit()
        session.refresh(student)
    else:
        raise HTTPException(status_code=404,detail="Student Not Found")
    
# ================= DELETE Method ================================

@app.delete("/delete-student/{student_id}")
def delete_student(student_id:int):
    session=get_session()

    student=session.get(Student,student_id)
    if not student:
        raise HTTPException(status_code=200,detail="Error: Delete not Performed / ID doesn't exists")
    session.delete(student)
    session.commit()

    return {f"Status: Id {student_id} Deleted Succesfully!"}