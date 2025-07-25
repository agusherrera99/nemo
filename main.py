import sqlite3

from pathlib import Path
from types import TracebackType

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


class Database:
    __connection = sqlite3.connect(DATABASEPATH)

    def __init__(self):
        self.__createTaskTable()

    def __getQueryFromSQLFile(self, filename: Path) -> str:
        with open(filename, mode="rt") as sqlfile:
            queryContent = sqlfile.read()
            return queryContent

    def __createTaskTable(self):
        query = self.__getQueryFromSQLFile(QUERIESDIRPATH / "createTaskTable.sql")
        with SafeCursor(self.__connection) as cursor:
            cursor.execute(query)
            self.__connection.commit()

    def GetTasksList(self) -> TasksTuplesList:
        query = self.__getQueryFromSQLFile(QUERIESDIRPATH / "getTasks.sql")

        with SafeCursor(self.__connection) as cursor:
            response = cursor.execute(query)
            tasksList = response.fetchall()

        return tasksList

    def AddTask(self, title: str, description: str, completed: bool = False):
        query = self.__getQueryFromSQLFile(QUERIESDIRPATH / "addTask.sql")
        params = (
            title,
            description,
            completed,
        )

        with SafeCursor(self.__connection) as cursor:
            cursor.execute(query, params)
            self.__connection.commit()
