# simple to-do app using FastAPI
# This code sets up a FastAPI application with static file serving and template rendering.

from fastapi import FastAPI, Request, Form 
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from pydantic import BaseModel, Field 
from fastapi import status
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uuid


app = FastAPI()

# Task model
class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    taskname: str = Field(..., example="Task 1")
    description: str = Field(..., example="Description of Task 1")
    duedate: str = Field(..., example="2023-10-01")

# Sample tasks for app
tasks = [
     {
        "id": str(uuid.uuid4()),
        "taskname": "Morning Jog",
        "description": "Run 5km around the park",
        "duedate": "2023-10-01"
     },
     {
        "id": str(uuid.uuid4()),
        "taskname": "Team Meeting",
        "description": "Weekly sync-up with the dev team",
        "duedate": "2023-10-02"
     },
     {
        "id": str(uuid.uuid4()),
        "taskname": "Grocery Shopping",
        "description": "Buy vegetables, fruits, and snacks",
        "duedate": "2023-10-03"
     },
     {
        "id": str(uuid.uuid4()),
        "taskname": "Read Book",
        "description": "Finish reading 'Clean Architecture'",
        "duedate": "2023-10-04"
     },
     {
        "id": str(uuid.uuid4()),
        "taskname": "Code Review",
        "description": "Review pull requests on GitHub",
        "duedate": "2023-10-05"
     }
]

# route for testing server 
@app.get("/")
def read_root():
    return HTMLResponse("<h1>Welcome to the TaskVault!</h1>")

# Static file serving
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template rendering
templates = Jinja2Templates(directory="templates")

#  route to render the main page
@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Include task routes
@app.get("/tasks")
async def get_tasks(request: Request):
    return templates.TemplateResponse("task.html", {"request": request, "tasks": tasks})


# Task routes
@app.get("/new-task")
async def new_task(request: Request):
    return templates.TemplateResponse("new.html", {"request": request})


# new task creation route
@app.post("/new_task")
async def create_task(request: Request):
    form_data = await request.form()
    taskname = form_data.get("taskname")
    description = form_data.get("description")
    duedate = form_data.get("duedate")

    if not taskname or not description or not duedate:
        return templates.TemplateResponse("new.html", {
            "request": request,
            "error": "All fields are required"
        })

    task = Task(
        taskname=taskname,
        description=description,
        duedate=duedate
    )
    tasks.append(task.dict())  

    return templates.TemplateResponse("task.html", {
        "request": request,
        "tasks": tasks  
    })

# Edit task route
#  gets edit form
@app.get("/edit-task/{task_id}", response_class=HTMLResponse)
async def edit_task_form(request: Request, task_id: str):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("edit.html", {"request": request, "task": task})

# post edit details to task route 
@app.post("/edit-task/{task_id}",)
async def edit_task(request: Request, task_id: str):
    form_data = await request.form()
    taskname = form_data.get("taskanme")
    description = form_data.get("description")
    duedate = form_data.get("duedate")

    if not taskname or not description or not duedate:
        return templates.TemplateResponse("edit.html", {
            "request": request,
            "error": "All fields are required"
        })
    
    task = Task(
        taskanme=taskname,
        description=description,
        duedate=duedate
    )

    tasks.append(task)

    return templates.TemplateResponse("task.html",{
        "request": request,
        "tasks": task
    })
