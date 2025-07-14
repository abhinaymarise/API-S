from fastapi import FastAPI,Path
from typing import Optional         
from pydantic import BaseModel  #===== For POST Method ==========


app=FastAPI()

#=========== Basic GET API Call ===============

@app.get("/")
def start():
    return{"call":"first_api"}

#========= Data for the Path Parameters =============== 

students={
    1:{
        "name":"Abhinay",
        "role":"SDE",
        "Salary":1000000
    },
    2:{
        "name":"Varshini",
        "role":"Data Analyst",
        "Salary":80000
    },
    3:{
        "name":"C",
        "role":"DevOps",
        "Salary":20000
    }
}

#============== Path Parameters ============================

@app.get("/students/{student_id}")
def path_param(student_id:int = Path(...,le=5,description="Enter the Student_Id",gt=0)):
    return students[student_id]

#============ Query Parameters ==========================

@app.get("/student-name")
def query_param(*,name:Optional[str] = None, test:int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data":"Not Found"}

#============ Combine Path and Query Parameters ============

@app.get("/student/{student_id}")
def path_com_query(*,student_id:int,name:str):
    for student_id in students:
        if students[student_id]["name"]==name:
            return students[student_id]
    return {"Data":"Not Found"}

#=============== POST Method =======================

class Student(BaseModel):
    name:str
    role:str
    salary:Optional[int]=None


#========== Create a New Entry using post method ==========

@app.post("/create-student/{student_id}")
def create_student(student_id:int,student:Student):
    if student_id in students:
        return{'Error':'Student Already Exists'}
    students[student_id]=student
    return students[student_id]

#======== Retrive the new user created using get method ==============

@app.get("/get-created-student/{student_id}")
def retrieve_created_student(student_id:int):
        if student_id in students:
            return students[student_id]
        return {"Error":"Data not found"}

#============= PUT Method =======================

class UpdateStudent(BaseModel):
    name:Optional[str]=None
    role:Optional[str]=None
    salary:Optional[int]=None

#=========== Update the existing data with PUT Method =============

@app.put("/update-student/{student_id}")
def update_student(student_id:int, student:UpdateStudent):
    if student_id not in students:
        return {"Error":"Data not Found"}
    if student.name != None:
        students[student_id].name=student.name
    if student.role != None:
        students[student_id].role=student.role
    if student.salary != None:
        students[student_id].salary=student.salary
    return students[student_id]

#================= Delete Method ===================

@app.delete("/delete_student/{student_id}")
def delete_student(student_id:int):
    if student_id in students:
        del students[student_id]
        return {"Message":"Successfully Deleted"}
    return {"Error":"Not Deleted or Not Exists"}