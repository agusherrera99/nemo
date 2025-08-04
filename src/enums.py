from enum import Enum

class States(object):
    @classmethod
    def validateValue(cls, value: int, minimum: int, maximum: int):
        if not (minimum <= value <= maximum):
            raise ValueError(f"{value} must be in range [{minimum, maximum}]")


class TaskPinStates(Enum, States):
    UNPINNED = 0
    PINNED = 1

    @classmethod
    def getPinStateValueByStr(cls, pintStateStr: str):
        try:
            stateValue = cls[pintStateStr].value
            cls.validateValue(value=stateValue, minimum=cls.UNPINNED.value, maximum=cls.PINNED.value)
            return stateValue
        except KeyError:
            raise ValueError(f"Invalid pin state: {pintStateStr}")


class TaskStates(Enum, States):
    INCOMPLETED = 0
    COMPLETED = 1
    IN_PROGRESS = 2

    @classmethod
    def getStateValueByStr(cls, stateStr: str):
        try:
            stateValue: int = cls[stateStr].value
            cls.validateValue(value=stateValue, minimum=cls.INCOMPLETED.value, maximum=cls.IN_PROGRESS.value)
            return stateValue
        except KeyError:
            raise ValueError(f"Invalid State: {stateStr}")