from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4

from main import generate_schedule
from typing import List

class Teacher(BaseModel):
    name:str

class Classroom(BaseModel):
    name:str

# Representa uma linha da matriz curricular
# Ex: { "teacher_id": "t1", "classroom_id": "c1", "count": 4 }
class Requirement(BaseModel):
    teacher_id: str
    classroom_id: str
    count: int

# Representa o pedido completo de geração
# Ex: { "slots": ["Seg8", "Seg9"], "requirements": [...] }
class ScheduleRequest(BaseModel):
    slots: List[str]
    requirements: List[Requirement]


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


@app.post("/generate-schedule")
def run_generation(request: ScheduleRequest):

    formated_reqs = []
    for req in request.requirements:
        formated_reqs.append((req.teacher_id,req.classroom_id,req.count))

    
    result = generate_schedule(
        teachers=db_teachers,
        classrooms=db_classrooms,
        slots=request.slots,
        requirements=formated_reqs
    )

    if result:
        return result
    else:
        return {"message": "Não foi possível gerar um horário com essas restrições."}