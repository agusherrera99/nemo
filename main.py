import sqlite3

from types import TracebackType

class SafeCursor:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def __enter__(self) -> sqlite3.Cursor:
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ):
        self.cursor.close()


