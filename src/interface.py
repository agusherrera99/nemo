from argparse import ArgumentParser, Namespace
from collections.abc import Sequence
from typing import Optional

from src.database import Database


class Interface:
    def __init__(self) -> None:
        self.database = Database()
        self.parser = ArgumentParser(prog="nemo", description="CLI task manager")

        self._setupArguments()

    def _setupList(self):
        self.subparsers.add_parser("list", help="Get tasks list")
    
    def _setupDelete(self):
        deleteSubparser = self.subparsers.add_parser("delete", help="Delete one task at a time or all of them")
        
        group = deleteSubparser.add_mutually_exclusive_group(required=True)
        
        group.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="Delete all tasks"
        )
        group.add_argument(
            "-u",
            "--uuid",
            type=str,
            help='Delete a task by passing his UUID; nemo delete -u "98c6078d"'
        )

    def _setupAdd(self):
        addSubparser = self.subparsers.add_parser("add", help="Add a new task")
        addSubparser.add_argument(
            "-t",
            "--title",
            type=str,
            default="untitle task",
            help='Task title (default: untitled task); e.g nemo add -t "some title"',
        )
        addSubparser.add_argument(
            "-d",
            "--description",
            type=str,
            default="no description provided",
            help='Task Description (default: no description provided); e.g nemo add -d "some description"',
        )

    def _setupUpdate(self):
        updateSubparser = self.subparsers.add_parser("update", help="Update task info")

        updateSubparser.add_argument(
            "-u",
            "--uuid",
            type=str,
            required=True,
            help='Indicate the task to update by its UUID; nemo update -u "2a712be5"'
        )

        updateSubparser.add_argument(
            "-t",
            "--title",
            type=str,
            help="Update the title of a task"
        )

        updateSubparser.add_argument(
            "-d",
            "--description",
            type=str,
            help="Update the description of a task"
        )

        updateSubparser.add_argument(
            "-s",
            "--state",
            choices=["completed", "incompleted", "in_progress"],
            help="Update the state of a task"
        )

    def _setupArguments(self):
        self.subparsers = self.parser.add_subparsers(
            dest="command", help="Available commands"
        )

        self._setupList()
        self._setupAdd()
        self._setupDelete()
        self._setupUpdate()

    def _handleGetTasksList(self):
        taskTupleList = self.database.getTasksTupleList()
        taskTupleListLength = len(taskTupleList)
        if taskTupleListLength > 0:
            for taskTuple in taskTupleList:
                _, hexUUID, title, description, status = taskTuple
                statusParse = "Incomplete" if status == 0 else "Completed"
                
                print(f"- {title.capitalize()} | {statusParse} | #{hexUUID}")
                print(f"\t{description.capitalize()}\n")
        else:
            print("There are not registered tasks")

    def _handleAdd(self, args: Namespace):
        title: str = args.title.lower()
        description: str = args.description.lower()

        print(f"Adding task: {title.capitalize()} {description.capitalize()}...")
        result = self.database.addTask(title, description)
        hexUUID: str = result[0]
        print(f"Task added successfully with UUID: #{hexUUID}")

    def _handleDelete(self, args: Namespace):
        if args.all:
            print("Deleting all tasks...")
            success = self.database.deleteAllTasks()
            if success:
                print("All tasks deleted successfully")
            else:
                print("Has occurred an error when delete all tasks, please try again")
        elif args.uuid:
            hexUUID = args.uuid

            print(f"Deleting task with UUID: #{hexUUID}...")
            success = self.database.deleteTask(hexUUID)
            if success:
                print("Deletion successfully")
            else:
                print("Has occurred an error when delete the task, please try again")
        else:
            print("Error: You must specify either -a/--all or -u/--uuid")
            print("Use 'nemo delete --help' for more information")

    def _handleUpdate(self, args: Namespace):
        hexUUID = args.uuid

        if args.title:
            newTitle: str = args.title
            print(f"Updating title of task: {hexUUID}...")
            success = self.database.updateTaskTitle(hexUUID, newTitle.lower())
            if success:
                print("Title updated successfully")
            else:
                print("Has occurred an error when update the title task, please try again")
        elif args.description:
            newDescription: str = args.description
            print(f"Updating description of task: {hexUUID}...")
            success = self.database.updateTaskDescription(hexUUID, newDescription.lower())
            if success:
                print("Description updated successfully")
            else:
                print("Has occurred an error when update the description task, please try again")
        elif args.state:
            newState: str = args.state
            print(f"Updating state of task: {hexUUID}...")
            success = self.database.updateTaskState(hexUUID, newState.upper())
            if success:
                print("State updated successfully")
            else:
                print("Has occurred an error when update the state task, please try again")

    def parseArgs(self, args: Optional[Sequence[str]] = None):
        return self.parser.parse_args(args)

    def execute(self, args: Optional[Sequence[str]] = None):
        parsedArgs = self.parseArgs(args)

        if parsedArgs.command == "list":
            self._handleGetTasksList()
        elif parsedArgs.command == "add":
            self._handleAdd(parsedArgs)
        elif parsedArgs.command == "delete":
            self._handleDelete(parsedArgs)
        elif parsedArgs.command == "update":
            self._handleUpdate(parsedArgs)
        else:
            self.parser.print_help()
