from enum import IntEnum


class WorkItemStatus(IntEnum):
    NEW = 0
    CLOSED = 1
    PAUSED = 2
    RUNNING = 3


class WorkItemType(IntEnum):
    PROJECT = 2
    COMPLEX_TASK = 1
    TASK = 0
