from unittest import TestCase
from src.database import Database

class DatabaseTestCase(TestCase):
    def setUp(self):
        self.database = Database()

    def tearDown(self) -> None:
        self.database.close()