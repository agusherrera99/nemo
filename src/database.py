import sqlite3

from pathlib import Path
from types import TracebackType
from typing import Optional, Union
from uuid import uuid4

from src.constants import DATABASEPATH, QUERIESDIRPATH


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


type TaskTuple = tuple[int, str, str, int]
type TasksTuplesList = list[TaskTuple]
type PathOrStr = Union[str, Path]

COMPLETED = 1
INCOMPLETED = 0


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

    def getTasksList(self) -> TasksTuplesList:
        query = self.__getQueryFromSQLFile("getTasks.sql")

        with SafeCursor(self.__connection) as cursor:
            response = cursor.execute(query)
            tasksList = response.fetchall()

        return tasksList

    def addTask(
        self,
        title: Optional[str] = "write your title here",
        description: Optional[str] = "write your description here",
        state: Optional[bool] = False,
    ) -> tuple[str]:
        query = self.__getQueryFromSQLFile("addTask.sql")
        randomUUID = uuid4()
        hexadecimalString = randomUUID.hex[:5]
        
        stateValue = COMPLETED if state else INCOMPLETED

        params = (
            hexadecimalString,
            title,
            description,
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

    def deleteTask(self, hexUUID: str):
        query = self.__getQueryFromSQLFile("deleteTask.sql")
        params = (hexUUID,)
        with SafeCursor(self.__connection) as cursor:
            cursor.execute(query, params)
            self.__connection.commit()

    def setTaskAsCompleted(self, hexUUID: str):
        query = self.__getQueryFromSQLFile("setTaskCompletedValue.sql")
        params = (COMPLETED, hexUUID)
        with SafeCursor(self.__connection) as cursor:
            cursor.execute(query, params)
            self.__connection.commit()

    def setTaskAsIncompleted(self, hexUUID: str):
        query = self.__getQueryFromSQLFile("setTaskCompletedValue.sql")
        params = (INCOMPLETED, hexUUID)
        with SafeCursor(self.__connection) as cursor:
            cursor.execute(query, params)
            self.__connection.commit()

    def close(self):
        if self.__connection:
            self.__connection.close()
