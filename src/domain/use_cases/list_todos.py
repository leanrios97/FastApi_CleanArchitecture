from typing import List
from domain.entities.todo import Todo
from domain.repositories.todo_repository import TodoRepository

class ListTodosUseCase: 
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    async def execute(self) -> List[Todo]: 
        return await self.repository.list_all()