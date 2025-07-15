from sqlalchemy import Column, Integer, String, Boolean, DateTime
from infrastructure.database.database import Base
from datetime import datetime, timezone

class TodoModel(Base): 
    __tablename__ = "Todos"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
