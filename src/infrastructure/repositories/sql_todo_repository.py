from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.todo import Todo
from domain.exceptions import TodoNotFoundError
from domain.repositories.todo_repository import TodoRepository
from infrastructure.database.models.todo_model import TodoModel
from config import logger

class SQLTodoRepository(TodoRepository): 
    def __init__(self, db: Session):
        self.db = db

    async def create(self, todo: Todo) -> Todo:
        db_todo = TodoModel(
            title = todo.title,
            description = todo.description, 
            completed = todo.completed, 
            created_at = todo.created_at 
        )
        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)
        logger.info(f"Task created successfully: id={db_todo.id}, title={db_todo.title}")


        return Todo(
            id = db_todo.id, 
            title=db_todo.title, 
            description= db_todo.description, 
            completed = db_todo.completed, 
            created_at = db_todo.created_at
        ) 
    
    async def get_by_id(self, todo_id: int) -> Optional[Todo]:
        db_todo = self.db.query(TodoModel).filter(TodoModel.id == todo_id).first()

        if not db_todo: 
            logger.error(f"Failed to get task: Todo with id={todo_id} not found")
            raise TodoNotFoundError()
        
        logger.info(f"Task retrieved successfully: id={db_todo.id}, title={db_todo.title}")

        return Todo(
            id = db_todo.id, 
            title=db_todo.title, 
            description= db_todo.description, 
            completed = db_todo.completed, 
            created_at = db_todo.created_at
        ) 
    
    async def list_all(self) -> List[Todo]:
        db_todos = self.db.query(TodoModel).all()
        logger.info(f"Retrieved {len(db_todos)} tasks")

        return [
            Todo(
            id = db_todo.id, 
            title=db_todo.title, 
            description= db_todo.description, 
            completed = db_todo.completed, 
            created_at = db_todo.created_at
            ) for db_todo in db_todos
        ]
        
    async def update_todo(self, todo: Todo) -> Todo: 
        db_todo = self.db.query(TodoModel).filter(TodoModel.id == todo.id).first()

        if not db_todo: 
            logger.error(f"Failed to update task: Todo with id={todo.id} not found")
            raise TodoNotFoundError()
        
        db_todo.title = todo.title
        db_todo.description = todo.description
        db_todo.completed = todo.completed

        self.db.commit()
        self.db.refresh(db_todo)
        logger.info(f"Task updated successfully: id={db_todo.id}, title={db_todo.title}")

        return Todo(
            id = db_todo.id, 
            title=db_todo.title, 
            description= db_todo.description, 
            completed = db_todo.completed, 
            created_at = db_todo.created_at
        ) 
    
    async def delete_todo(self, todo_id: int) -> None: 
        db_todo = self.db.query(TodoModel).filter(TodoModel.id == todo_id).first()

        if not db_todo: 
            logger.error(f"Failed to delete task: Todo with id={todo_id} not found")
            raise TodoNotFoundError()
        
        self.db.delete(db_todo)
        self.db.commit()
        logger.info(f"Task deleted successfully: id={todo_id}")