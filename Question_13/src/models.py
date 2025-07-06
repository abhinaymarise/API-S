from sqlmodel import SQLModel,Field
from typing import Optional
from pydantic import BaseModel,ConfigDict

class Student(SQLModel,table=True):
    id:int=Field(primary_key=True)
    Name: str
    Age : int
    Email: Optional[str]=None
    Country: str

class StudentResponse(BaseModel):
    id:int=Field(primary_key=True)
    Name: str
    Age : int
    Email: Optional[str]=None
    Country: str

#===== In order to ensure the order of attributes in given manner ===========

    model_config=ConfigDict(from_attributes=True)
