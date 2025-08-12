import sqlite3

from datetime import datetime, timedelta
from pathlib import Path
from types import TracebackType
from typing import Optional, Union
from uuid import uuid4

from src.constants import DATABASEPATH, QUERIESDIRPATH
from src.enums import TaskPinStates, TaskStates


class SafeCursor:
    def __init__(self, connection: sqlite3.Connection):
        self.__connection = connection

    def __enter__(self) -> sqlite3.Cursor:
        self.cursor = self.__connection.cursor()
        return self.cursor

    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ):
        self.cursor.close()


type TaskTuple = tuple[int, str, str, str, str, int, int]
type TasksTuplesList = list[TaskTuple]
type PathOrStr = Union[str, Path]


class Database:
    def __init__(self, databasePath: Optional[PathOrStr] = None):
        if databasePath is None:
            databasePath = DATABASEPATH
        self.__connection = sqlite3.connect(databasePath)
        self.__createTaskTable()

    def __getQueryFromSQLFile(self, filename: str) -> str:
        filepath = QUERIESDIRPATH / filename
        with open(filepath, mode="rt") as sqlfile:
            queryContent = sqlfile.read()
            return queryContent

    def __createTaskTable(self):
        query = self.__getQueryFromSQLFile("createTaskTable.sql")
        with SafeCursor(self.__connection) as cursor:
            cursor.execute(query)
            self.__connection.commit()

    def _getEstimatedDeadlineDatetime(self, daysUntilDeadline: Optional[int]) -> Optional[datetime]:
        if daysUntilDeadline:
            today = datetime.today()
            deadlineDatetime = today + timedelta(daysUntilDeadline)
            return deadlineDatetime
        return None

    def _pinnedFirst(self, taskTuple: TaskTuple) -> bool:
        pinStateValue = int(taskTuple[5])
        isPinned = pinStateValue == TaskPinStates.PINNED.value
        return isPinned
    
    def getEstimatedDatetime(self, hexUUID: str) -> str:
        query = self.__getQueryFromSQLFile("getEstimatedDeadline.sql")

        params = (hexUUID,)
        with SafeCursor(self.__connection) as cursor:
            response = cursor.execute(query, params)
            result = response.fetchone()
            if result is None:
                raise sqlite3.Error("estimated datetime not found")

        return result[0]

    def getTasksTupleList(self) -> TasksTuplesList:
        query = self.__getQueryFromSQLFile("getTasks.sql")

        with SafeCursor(self.__connection) as cursor:
            response = cursor.execute(query)
            tasksTupleList = response.fetchall()

        tasksTupleList.sort(
            key=self._pinnedFirst,
            reverse=True,
        )

        return tasksTupleList

    def addTask(
        self, title: str, description: str, estimatedDeadline: Optional[int] = None
    ) -> tuple[str]:
        query = self.__getQueryFromSQLFile("addTask.sql")
        randomUUID = uuid4()
        hexadecimalString = randomUUID.hex[:8]
        estimatedDatetime: datetime | None = self._getEstimatedDeadlineDatetime(
            estimatedDeadline
        )

        stateValue = TaskStates.INCOMPLETED.value

        params = (
            hexadecimalString,
            title,
            description,
            estimatedDatetime,
            TaskPinStates.UNPINNED.value,
            stateValue,
        )

        with SafeCursor(self.__connection) as cursor:
            response = cursor.execute(query, params)
            result = response.fetchone()
            if result is None:
                raise sqlite3.Error("task insertion should return UUID value")
            self.__connection.commit()

        return result

    def deleteAllTasks(self):
        query = self.__getQueryFromSQLFile("deleteAllTasks.sql")
        with SafeCursor(self.__connection) as cursor:
            cursor.execute(query)
            self.__connection.commit()

        tasksTupleList = self.getTasksTupleList()
        success = True if len(tasksTupleList) else False
        return success

    def deleteTask(self, hexUUID: str) -> bool:
        query = self.__getQueryFromSQLFile("deleteTask.sql")
        params = (hexUUID,)
        with SafeCursor(self.__connection) as cursor:
            response = cursor.execute(query, params)
            result = response.fetchone()
            if result is None:
                raise sqlite3.Error("task deletion should return UUID value")
            self.__connection.commit()

        success = True if result[0] else False
        return success

    def updateTaskTitle(self, hexUUID: str, newTitle: str) -> bool:
        query = self.__getQueryFromSQLFile("updateTaskTitleValue.sql")

        params = (newTitle, hexUUID)
        with SafeCursor(self.__connection) as cursor:
            response = cursor.execute(query, params)
            result = response.fetchone()
            if result is None:
                raise sqlite3.Error("title task update should return UUID value")
            self.__connection.commit()

        success = True if result[0] else False
        return success

    def updateTaskDescription(self, hexUUID: str, newDescription: str) -> bool:
        query = self.__getQueryFromSQLFile("updateTaskDescriptionValue.sql")

        params = (newDescription, hexUUID)
        with SafeCursor(self.__connection) as cursor:
            response = cursor.execute(query, params)
            result = response.fetchone()
            if result is None:
                raise sqlite3.Error("description task update should return UUID value")
            self.__connection.commit()

        success = True if result[0] else False
        return success

    def updateTaskEstimatedDeadline(self, hexUUID: str, newDaysUntilDeadline: int) -> bool:
        query = self.__getQueryFromSQLFile("updateTaskEstimatedDeadline.sql")

        actualEstimatedDatetime = datetime.strptime(
            self.getEstimatedDatetime(hexUUID), "%Y-%m-%d %H:%M:%S.%f"
        )

        newEstimatedDeadline = None
        if newDaysUntilDeadline < 0:
            newEstimatedDeadline = actualEstimatedDatetime - timedelta(abs(newDaysUntilDeadline))
        elif newDaysUntilDeadline > 0:
            newEstimatedDeadline = actualEstimatedDatetime + timedelta(newDaysUntilDeadline)
        else:
            newEstimatedDeadline = actualEstimatedDatetime


        params = (newEstimatedDeadline, hexUUID)
        with SafeCursor(self.__connection) as cursor:
            response = cursor.execute(query, params)
            result = response.fetchone()
            if result is None:
                raise sqlite3.Error("estimatedDeadline update should return UUID value")
            self.__connection.commit()

        success = True if result[0] else False
        return success

    def updateTaskPin(self, hexUUID: str, newPinState: str) -> bool:
        query = self.__getQueryFromSQLFile("updateTaskPinStateValue.sql")

        pinStateValue = TaskPinStates.getPinStateValueByStr(newPinState)

        params = (pinStateValue, hexUUID)
        with SafeCursor(self.__connection) as cursor:
            response = cursor.execute(query, params)
            result = response.fetchone()
            if result is None:
                raise sqlite3.Error("pin state task update should return UUID value")
            self.__connection.commit()

        success = True if result[0] else False
        return success

    def updateTaskState(self, hexUUID: str, newState: str) -> bool:
        query = self.__getQueryFromSQLFile("updateTaskStateValue.sql")

        stateValue = TaskStates.getStateValueByStr(newState)

        params = (stateValue, hexUUID)
        with SafeCursor(self.__connection) as cursor:
            response = cursor.execute(query, params)
            result = response.fetchone()
            if result is None:
                raise sqlite3.Error("state task update should return UUID value")
            self.__connection.commit()

        success = True if result[0] else False
        return success

    def close(self):
        if self.__connection:
            self.__connection.close()
