from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.todo import Todo

class TodoRepository(ABC): 

    @abstractmethod
    async def create(self, todo: Todo) -> Todo: 
        pass 

    @abstractmethod
    async def get_by_id(seld, todo_id: int) -> Optional[Todo]: 
        pass

    @abstractmethod
    async def list_all(self) -> List[Todo]: 
        pass 

    @abstractmethod 
    async def update_todo(self, todo: Todo) -> Todo: 
        pass 

    @abstractmethod
    async def delete_todo(self, todo_id: int) -> None:
        pass