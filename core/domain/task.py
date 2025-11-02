from datetime import datetime

import dataclasses
from .status import Status



@dataclasses.dataclass
class Task:
    # Заголовок задачи.
    title: str

    # Описание задачи.
    description: str | None

    # Статус задачи: Не начато, В процессе, Сделано
    status: Status

    async def change_status(self, to_status: Status):
        from_status = self.status

        if from_status == to_status:
            raise InvalidStatusChangeException(from_status, to_status)
        
        self.status = to_status
        

@dataclasses.dataclass
class TaskRecord(Task):
    # Уникальный ID задачи.
    id: int

    # Время создания задачи.
    opened_at: datetime | None

    # Время последнего объявления задачи.
    updated_on: datetime | None


class InvalidStatusChangeException(Exception):
    def __init__(self, cur_status, to_status):
        super().__init__(f"Invalid change from status: = {cur_status} to {to_status}")