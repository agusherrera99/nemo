from src.database import Database
from unittest import TestCase
from unittest.mock import patch

class TestDatabase(TestCase):
    def setUp(self):
        with patch("src.constants.DATABASEPATH", ":memory:"):
            self.database = Database()

    def tearDown(self) -> None:
        self.database.close()

    def test_add_task_successfully(self):
        title = "title sample"
        description = "description sample"

        result = self.database.addTask(title, description)
        self.assertIsInstance(result, int)

    def test_get_tasks_list_empty(self):
        tasks = self.database.getTasksList()
        self.assertEqual(tasks, [])

    def test_get_tasks_list_with_tasks(self):
        self.database.addTask("Test Title", "Test Description")
        tasks = self.database.getTasksList()
        self.assertGreater(len(tasks), 0)

    def test_delete_all_tasks(self):
        self.database.addTask("Test Title", "Test Description")
        self.database.deleteAllTasks()
        tasks = self.database.getTasksList()
        self.assertEqual(len(tasks), 0)

    def test_add_multiple_tasks(self):
        task1 = self.database.addTask("Title 1", "Description 1")
        task2 = self.database.addTask("Title 2", "Description 2")
        
        self.assertIsInstance(task1, int)
        self.assertIsInstance(task2, int)
        self.assertNotEqual(task1, task2)