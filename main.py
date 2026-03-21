from fastapi import FastAPI 
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


# =====================================================GET REQUESTS===================================================================
@app.get("/")
def read_root():
    return {"Message" : "Hello! I am Aradhya"}

@app.get("/greet")
def greet_message():
    return {"Message" : "Good Morning/Afternoon/Evening"}

@app.get("/greet/{name}")
def new_name(name: str, age: Optional[int] = None):
    return {"Message" : f"Hello {name} and my age is {age} years"}


# =====================================================POST REQUESTS===================================================================

class Student(BaseModel):
    name: str
    age: int
    roll: int


@app.post("/create_student")
def create_student(student: Student):
    return {
        "name": student.name,
        "age": student.age,
        "roll_no": student.roll

    }
