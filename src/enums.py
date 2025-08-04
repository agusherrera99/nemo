from enum import Enum


class TaskPinStates(Enum):
    UNPINNED = 0
    PINNED = 1

    @classmethod
    def getPinStateValueByStr(cls, pintStateStr: str):
        try:
            pinStateValue = cls[pintStateStr].value
            return pinStateValue
        except KeyError:
            validPinStates = [pinState.name for pinState in cls]
            raise ValueError(f"Invalid pin state: {pintStateStr}. Valid states: {validPinStates}")


class TaskStates(Enum):
    INCOMPLETED = 0
    COMPLETED = 1
    IN_PROGRESS = 2

    @classmethod
    def getStateValueByStr(cls, stateStr: str):
        try:
            stateValue: int = cls[stateStr].value
            return stateValue
        except KeyError:
            validStates = [state.name for state in cls]
            raise ValueError(f"Invalid pin state: {stateStr}. Valid states: {validStates}")