from typing import Optional
from domain.entities.todo import Todo
from domain.repositories.todo_repository import TodoRepository

class GetTodoUseCase: 
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    async def execute(self, todo_id: int) -> Optional[Todo]: 
        return await self.repository.get_by_id(todo_id)
    
        