from enum import IntEnum


class WorkItemStatus(IntEnum):
    NEW = 0
    CLOSED = 1
    PAUSED = 2
    RUNNING = 3


class WorkItemType(IntEnum):
    project = 2
    FEATURE = 1
    TASK = 0
