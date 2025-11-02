import enum


class Status(str, enum.Enum):
    TODO          = "Не начато"
    IN_PROGRESS   = "В процессе"
    DONE          = "Сделано"