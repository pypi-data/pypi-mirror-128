from enum import Enum


class State(Enum):
    QUEUED = 0
    RUNNING = 1
    SUCCESS = 2
    FAILED = 3
