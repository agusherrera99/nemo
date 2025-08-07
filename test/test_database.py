from src.database import Database
from unittest import TestCase


class TestDatabase(TestCase):
    def setUp(self):
        self.database = Database(":memory:")

    def tearDown(self) -> None:
        self.database.close()

    def _get_tasks_count(self) -> int:
        return len(self.database.getTasksTupleList())

    def _assert_tasks_count(self, expectedCount: int, message: str = ""):
        actualCount = self._get_tasks_count()

        if message == "":
            message = f"Expected {expectedCount} tasks, got {actualCount}"

        self.assertEqual(actualCount, expectedCount, message)

    def test_add_task(self):
        self._assert_tasks_count(0)

        result = self.database.addTask("test title", "test description", 2)
        hexUUID = result[0]
        self.assertIsNotNone(hexUUID)

        self._assert_tasks_count(1)

    def test_add_multiple_tasks(self):
        self._assert_tasks_count(0)

        task1 = self.database.addTask("title 1", "description 1", 2)
        task2 = self.database.addTask("title 2", "description 2", 2)
        self._assert_tasks_count(2)

        self.assertIsNotNone(hexUUID1 := task1[0])
        self.assertIsNotNone(hexUUID2 := task2[0])
        self.assertNotEqual(hexUUID1, hexUUID2)

    def test_get_tasks_list_empty(self):
        tasks = self.database.getTasksTupleList()
        self.assertEqual(tasks, [])

    def test_get_tasks_list_with_tasks(self):
        self.database.addTask("test title", "test description", 2)
        tasks = self.database.getTasksTupleList()
        self.assertGreater(len(tasks), 0)

    def test_delete_task(self):
        self._assert_tasks_count(0)

        addResult = self.database.addTask("test title", "test description", 2)
        self._assert_tasks_count(1)

        hexUUID = addResult[0]
        deleteResult = self.database.deleteTask(hexUUID)
        self.assertTrue(deleteResult, "successfull task deletion should return True")

        self._assert_tasks_count(0)

    def test_delete_all_tasks(self):
        self._assert_tasks_count(0)

        self.database.addTask("test title 1", "test description 1", 2)
        self.database.addTask("test title 1", "test description 1", 2)
        self.database.addTask("test title 1", "test description 1", 2)
        self._assert_tasks_count(3)

        self.database.deleteAllTasks()
        self._assert_tasks_count(0)

    def test_update_task_title(self):
        self._assert_tasks_count(0)

        result = self.database.addTask("test title", "test description")
        taskHexUUID = result[0]
        self._assert_tasks_count(1)
        taskTupleList = self.database.getTasksTupleList()
        oldTitle = taskTupleList[0][2]

        self.database.updateTaskTitle(taskHexUUID, "New title")
        taskTupleList = self.database.getTasksTupleList()
        newTitle = taskTupleList[0][2]

        self.assertNotEqual(oldTitle, newTitle)

    def test_update_task_description(self):
        self._assert_tasks_count(0)

        result = self.database.addTask("test title", "test description")
        taskHexUUID = result[0]
        self._assert_tasks_count(1)
        taskTupleList = self.database.getTasksTupleList()
        oldDescription = taskTupleList[0][3]

        self.database.updateTaskDescription(taskHexUUID, "New description")
        taskTupleList = self.database.getTasksTupleList()
        newDescription = taskTupleList[0][3]

        self.assertNotEqual(oldDescription, newDescription)

    def test_update_task_estimated_time(self):
        self._assert_tasks_count(0)

        result = self.database.addTask("test title", "test descripiton", 2)
        taskHexUUID = result[0]
        self._assert_tasks_count(1)

        taskTupleList = self.database.getTasksTupleList()
        oldEstimatedTime = taskTupleList[0][4]

        self.database.updateTaskEstimatedTime(taskHexUUID, 4)
        newEstimatedTime = taskTupleList[0][4]

        self.assertNotEqual(oldEstimatedTime, newEstimatedTime)

    def test_update_task_pin_state(self):
        self._assert_tasks_count(0)

        result = self.database.addTask("test title", "test description")
        taskHexUUID = result[0]
        self._assert_tasks_count(1)
        taskTupleList = self.database.getTasksTupleList()
        oldPinState = taskTupleList[0][5]

        self.database.updateTaskPinState(taskHexUUID, "PINNED")
        taskTupleList = self.database.getTasksTupleList()
        newPinState = taskTupleList[0][5]

        self.assertNotEqual(oldPinState, newPinState)

    def test_update_task_state(self):
        self._assert_tasks_count(0)

        result = self.database.addTask("test title", "test description")
        taskHexUUID = result[0]
        self._assert_tasks_count(1)
        taskTupleList = self.database.getTasksTupleList()
        oldTaskState = taskTupleList[0][6]

        self.database.updateTaskState(taskHexUUID, "IN_PROGRESS")
        taskTupleList = self.database.getTasksTupleList()
        newTupleState = taskTupleList[0][6]

        self.assertNotEqual(oldTaskState, newTupleState)
