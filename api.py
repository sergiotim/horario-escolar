from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4

class Teacher(BaseModel):
    name:str

class Classroom(BaseModel):
    name:str



# Instanciamos o aplicativo
app = FastAPI()

db_teachers = []
db_classrooms = []

# Decorator: Diz ao FastAPI que se alguém acessar a raiz "/" usando GET...
@app.get("/")
def home():
    # ... deve executar esta função e retornar este JSON
    return {"message": "Bem-vindo ao SmartSchedule API"}


@app.get("/teachers")
def list_teachers():
    return db_teachers

@app.post("/teachers")
def create_teacher(teacher:Teacher):
    id = str(uuid4())

    new_teacher = {
        "id": id,
        "name" : teacher.name
    }


    db_teachers.append(new_teacher)


    return new_teacher


@app.get("/classrooms")
def list_classrooms():
    return db_classrooms


@app.post("/classrooms")
def create_classroom(classromm:Classroom):
    id = str(uuid4())

    new_classroom = {
        "id":id,
        "name":classromm.name
    }

    db_classrooms.append(new_classroom)

    return new_classroom