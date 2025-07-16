from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import List
from domain.entities.todo import Todo
from domain.use_cases.create_todo import CreateTodoUseCase
from domain.use_cases.get_todo import GetTodoUseCase
from domain.use_cases.list_todos import  ListTodosUseCase
from domain.use_cases.update_todo import UpdateTodoUseCase
from domain.use_cases.delete_todo import DeleteTodoUseCase
from domain.repositories.todo_repository import TodoRepository
from domain.exceptions import TodoNotFoundError
from presentation.dependencies import get_todo_repository
from config import logger


router = APIRouter()

class TodoCreate(BaseModel): 
    title: str
    description: str

class TodoUpdate(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

class TodoResponse(BaseModel): 
    id: int
    title: str
    description: str
    completed: bool
    created_at: str


@router.post("/todos", response_model= TodoResponse)
async def create_todo(
    todo: TodoCreate, 
    repository: TodoRepository = Depends(get_todo_repository),
    request: Request = None
): 
    create_use_case = CreateTodoUseCase(repository)
    try: 
        result = await create_use_case.execute(todo.title, todo.description)
        logger.info(f"[{request.url.path}] Task created successfully: id={result.id}, title={result.title}")

        return TodoResponse(
            id = result.id,
            title = result.title,
            description = result.description, 
            completed = result.completed, 
            created_at = result.created_at.isoformat(),
            )
    
    except Exception as e: 
        logger.error(f"[{request.url.path}] Failed to create task: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int, 
    repository: TodoRepository = Depends(get_todo_repository),
    request: Request = None
    ):
    get_use_case = GetTodoUseCase(repository)
    try:
        result = await get_use_case.execute(todo_id)
        if not result:
            logger.error(f"[{request.url.path}] Failed to get task: Todo not found")
            raise TodoNotFoundError()
        
        logger.info(f"[{request.url.path}] Task retrieved successfully: id={result.id}, title={result.title}")
        return TodoResponse(
            id=result.id,
            title=result.title,
            description=result.description,
            completed=result.completed,
            created_at=result.created_at.isoformat()
        )
    except TodoNotFoundError as e:
        logger.error(f"[{request.url.path}] Failed to get task: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        logger.error(f"[{request.url.path}] Failed to get task: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/todos", response_model=List[TodoResponse])
async def list_todo(
    repository: TodoRepository = Depends(get_todo_repository),
    request: Request = None
): 
    
    list_use_case = ListTodosUseCase(repository)
    try: 
        results = await list_use_case.execute()
        logger.info(f"[{request.url.path}] Retrieved {len(results)} tasks")
    
        return [
            TodoResponse(
            id = todo.id,
            title = todo.title,
            description = todo.description, 
            completed = todo.completed, 
            created_at = todo.created_at.isoformat(),
            ) for todo in results
        ]
    
    except Exception as e:
        logger.error(f"[{request.url.path}] Failed to list tasks: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/todos", response_model=TodoResponse)
async def update_todo(
    todo: TodoUpdate,
    repository: TodoRepository = Depends(get_todo_repository),
    request: Request = None
): 
    
    update_use_case = UpdateTodoUseCase(repository)
    try:
        result = await update_use_case.execute(Todo(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            created_at=None
        ))

        logger.info(f"[{request.url.path}] Task updated successfully: id={result.id}, title={result.title}")

        return TodoResponse(
            id=result.id,
            title=result.title,
            description=result.description,
            completed=result.completed,
            created_at=result.created_at.isoformat()
        )
    
    except TodoNotFoundError as e:
        logger.error(f"[{request.url.path}] Failed to update task: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        logger.error(f"[{request.url.path}] Failed to update task: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: int, 
    repository: TodoRepository = Depends(get_todo_repository),
    request: Request = None
    ): 

    delete_use_case = DeleteTodoUseCase(repository)
    try:
        await delete_use_case.execute(todo_id)
        logger.info(f"[{request.url.path}] Task deleted successfully: id={todo_id}")
        return None
    
    except TodoNotFoundError as e:
        logger.error(f"[{request.url.path}] Failed to delete task: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        logger.error(f"[{request.url.path}] Failed to delete task: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))