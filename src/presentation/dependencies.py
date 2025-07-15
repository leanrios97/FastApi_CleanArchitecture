from fastapi import Depends
from sqlalchemy.orm import Session
from domain.repositories.todo_repository import TodoRepository
from infrastructure.repositories.sql_todo_repository import SQLTodoRepository
from infrastructure.database.database import get_db

def get_todo_repository(db: Session = Depends(get_db)) -> TodoRepository:
    return SQLTodoRepository(db)