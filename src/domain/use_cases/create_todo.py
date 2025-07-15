from datetime import datetime, timezone
from domain.entities.todo import Todo
from domain.repositories.todo_repository import TodoRepository

class CreateTodoUseCase:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    async def execute(self, title: str, description: str) -> Todo: 
        todo = Todo(
            id= None, 
            title=title, 
            description=description, 
            completed=False,
            created_at=datetime.now(timezone.utc)
        )
        return await self.repository.create(todo)
    
    
        
        