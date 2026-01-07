from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session
from ..models.task_model import Task, TaskCreate, TaskUpdate
from ..services.task_service import TaskService
from ..database import get_session
from ..auth.jwt_auth import get_current_user
from ..models.user_model import User

router = APIRouter(prefix="/api/v1", tags=["tasks"])


@router.get("/tasks", response_model=List[Task])
def get_tasks(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    tasks = TaskService.get_user_tasks(current_user.id, session)
    return tasks


@router.post("/tasks", response_model=Task)
def create_task(task_data: TaskCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = TaskService.create_task_for_user(task_data, current_user.id, session)
    return task


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = TaskService.get_task_by_id_for_user(task_id, current_user.id, session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = TaskService.update_task_for_user(task_id, task_data, current_user.id, session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    success = TaskService.delete_task_for_user(task_id, current_user.id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


# Specific endpoint for toggling completion status
@router.patch("/tasks/{task_id}/toggle-completion", response_model=Task)
def toggle_task_completion(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = TaskService.toggle_task_completion_for_user(task_id, current_user.id, session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task