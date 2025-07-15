from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Todo: 
    id: Optional[int]
    title: str
    description: str
    completed: bool
    created_at: datetime