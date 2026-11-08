
from fastapi import FastAPI, HTTPException, status, Query, Response
from app.schemas import TaskCreate, TaskUpdate, TaskStatusUpdate, TaskResponse
from typing import Literal


# =====================================
# APPLICATION INITIALIZATION
# =====================================

app = FastAPI(
    title="Task Management API",
    description="A simple REST API built using FastAPI",
    version="1.0.0"
)


# =====================================
# IN-MEMORY STORAGE
# =====================================

tasks = {}

next_task_id = 1


# =====================================
# 1. HOME ENDPOINT
# =====================================

@app.get("/")
def home():
    return {
        "message": "Welcome to Task Management API"
    }


# =====================================
# 2. ABOUT ENDPOINT
# =====================================

@app.get("/about")
def about():
    return {
        "project": "Task Management API",
        "version": "1.0.0",
        "developer": "FastAPI Student"
    }


# =====================================
# 3. CREATE A TASK (POST)
# =====================================

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(task: TaskCreate):

    global next_task_id

    new_task = {
        "id": next_task_id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "completed": task.completed
    }

    tasks[next_task_id] = new_task

    next_task_id += 1

    return new_task


# =====================================
# 4. GET ALL TASKS (GET)
# =====================================

@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def get_all_tasks():

    return list(tasks.values())


# =====================================
# 5. GET TASK BY ID (GET)
# =====================================

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task_by_id(task_id: int):

    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return tasks[task_id]


# =====================================
# 6. UPDATE TASK COMPLETELY (PUT)
# =====================================

@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(task_id: int, task: TaskUpdate):

    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    updated_task = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "completed": task.completed
    }

    tasks[task_id] = updated_task

    return updated_task


# =====================================
# 7. DELETE TASK (DELETE)
# =====================================

@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int):

    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    del tasks[task_id]

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# =====================================
# 8. UPDATE TASK STATUS (PATCH)
# =====================================

@app.patch(
    "/tasks/{task_id}/status",
    response_model=TaskResponse
)
def update_task_status(task_id: int, status_data: TaskStatusUpdate):

    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    tasks[task_id]["completed"] = status_data.completed

    return tasks[task_id]


# =====================================
# 9. FILTER TASKS (GET)
# =====================================

@app.get(
    "/tasks/filter",
    response_model=list[TaskResponse]
)
def filter_tasks(
    completed: bool | None = None,
    priority: Literal["low", "medium", "high"] | None = None
):

    filtered_tasks = list(tasks.values())

    if completed is not None:
        filtered_tasks = [
            task for task in filtered_tasks
            if task["completed"] == completed
        ]

    if priority is not None:
        filtered_tasks = [
            task for task in filtered_tasks
            if task["priority"] == priority
        ]

    return filtered_tasks
