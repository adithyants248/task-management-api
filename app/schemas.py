
from pydantic import BaseModel, Field
from typing import Literal


# 1. Schema for creating a task
class TaskCreate(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    description: str | None = None
    priority: Literal["low", "medium", "high"] = "low"
    completed: bool = False


# 2. Schema for updating a task completely (PUT)
class TaskUpdate(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    description: str | None
    priority: Literal["low", "medium", "high"]
    completed: bool


# 3. Schema for updating task completion status (PATCH)
class TaskStatusUpdate(BaseModel):
    completed: bool


# 4. Schema for returning task information
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    priority: Literal["low", "medium", "high"]
    completed: bool
