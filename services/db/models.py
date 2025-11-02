from datetime import datetime
from typing import cast

from sqlalchemy import Column, BigInteger, DateTime, Text, Enum, Integer

from core import domain
from services.db.base import Base


class BaseModel(Base):
    __abstract__ = True

    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Task(BaseModel):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    title           = Column(Text, nullable=False)
    description     = Column(Text, nullable=True)
    status          = Enum(domain.Status)
    
    @classmethod
    def from_domain(cls, task: domain.Task) -> "Task":
        """
        task: domain.Task - задача из core слоя
        return: Task
        """
        return Task(
            title           = task.title,
            description     = task.description,
            status          = task.status
        )
    
    def to_domain(self) -> domain.TaskRecord:
        """
        return: domain.TaskRecord - возвращает задачу в формате domain.TaskRecord
        """
        return domain.TaskRecord(
            id                          = cast(int, self.id),
            title                       = cast(str, self.title),
            description                 = cast(str | None, self.description),
            status                      = cast(domain.Status, self.status),
            opened_at                   = cast(datetime | None, self.created_on),
            updated_on                  = cast(datetime | None, self.updated_on)
        )