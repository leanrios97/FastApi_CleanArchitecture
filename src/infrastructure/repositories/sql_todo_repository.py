from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.todo import Todo
from domain.repositories.todo_repository import TodoRepository
from infrastructure.database.models.todo_model import TodoModel

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
            return None
        
        return Todo(
            id = db_todo.id, 
            title=db_todo.title, 
            description= db_todo.description, 
            completed = db_todo.completed, 
            created_at = db_todo.created_at
        ) 
    
    async def list_all(self) -> List[Todo]:
        db_todos = self.db.query(TodoModel).all()

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
            raise ValueError("Todo not found")
        
        db_todo.title = todo.title
        db_todo.description = todo.description
        db_todo.completed = todo.completed

        self.db.commit()
        self.db.refresh(db_todo)

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
            raise ValueError("Todo not found")
        
        self.db.delete(db_todo)
        self.db.commit()