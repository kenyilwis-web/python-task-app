"""
main.py
Entry point for the Task Management System.
Provides an interactive, menu-driven interface for managing tasks.
"""

from task_manager import task_utils, validation


def display_menu():
    """Prints the main menu to the console."""
    print("\n" + "=" * 45)
    print("       TASK MANAGEMENT SYSTEM")
    print("=" * 45)
    print("  1. Add a new task")
    print("  2. Mark a task as complete")
    print("  3. View pending tasks")
    print("  4. View all tasks")
    print("  5. Track progress")
    print("  6. Exit")
    print("=" * 45)


def prompt_task_title():
    """
    Prompts the user to enter a task title and validates the input.

    Returns:
        str: A validated, non-empty task title.
    """
    while True:
        title = input("  Enter task title: ")
        is_valid, error = validation.validate_task_title(title)
        if is_valid:
            return title.strip()
        print(f"  [Error] {error}")


def prompt_task_description():
    """
    Prompts the user to enter an optional task description and validates it.

    Returns:
        str: A validated task description (may be empty).
    """
    while True:
        description = input("  Enter description (optional, press Enter to skip): ")
        is_valid, error = validation.validate_task_description(description)
        if is_valid:
            return description.strip()
        print(f"  [Error] {error}")


def prompt_task_id(tasks):
    """
    Prompts the user to enter a task ID and validates that it exists.

    Args:
        tasks (list): The current list of task dictionaries.

    Returns:
        int: A validated task ID that exists in the task list.
    """
    while True:
        task_id = input("  Enter task ID: ")
        is_valid, error = validation.validate_task_id(task_id, tasks)
        if is_valid:
            return int(task_id)
        print(f"  [Error] {error}")


def prompt_due_date():
    """
    Prompts the user to enter an optional due date and validates the format.

    Returns:
        str: A validated due date string in YYYY-MM-DD format, or empty string.
    """
    while True:
        due_date = input("  Enter due date YYYY-MM-DD (optional, press Enter to skip): ")
        is_valid, error = validation.validate_due_date(due_date)
        if is_valid:
            return due_date.strip()
        print(f"  [Error] {error}")


def handle_add_task(tasks):
    """Handles the 'Add a new task' menu option."""
    print("\n--- Add New Task ---")
    title = prompt_task_title()
    description = prompt_task_description()
    due_date = prompt_due_date()
    try:
        new_task = task_utils.add_task(tasks, title, description, due_date)
        print(f"\n  Task #{new_task['id']} '{new_task['title']}' added successfully.")
    except (ValueError, TypeError) as exc:
        print(f"\n  [Error] Could not add task: {exc}")


def handle_complete_task(tasks):
    """Handles the 'Mark a task as complete' menu option."""
    print("\n--- Mark Task as Complete ---")

    pending = task_utils.view_pending_tasks(tasks)
    if not pending:
        print("  There are no pending tasks to complete.")
        return

    # Show pending tasks so the user knows which IDs are available
    print(f"\n  {'ID':<5} {'Title'}")
    print("  " + "-" * 35)
    for task in pending:
        print(f"  {task['id']:<5} {task['title']}")

    task_id = prompt_task_id(tasks)
    try:
        result = task_utils.mark_task_as_complete(tasks, task_id)
    except ValueError as exc:
        print(f"\n  [Error] {exc}")
        return

    if result is None:
        print(f"  Task #{task_id} is already marked as complete.")
    elif result:
        # Find the task title for a friendly confirmation message
        title = next(t["title"] for t in tasks if t["id"] == task_id)
        print(f"\n  Task #{task_id} '{title}' marked as complete.")
    else:
        print(f"  [Error] Could not update task #{task_id}.")


def handle_view_pending(tasks):
    """Handles the 'View pending tasks' menu option."""
    print("\n--- Pending Tasks ---")
    pending = task_utils.view_pending_tasks(tasks)
    if not pending:
        print("  No pending tasks. Great job!")
        return

    print(f"\n  {'ID':<5} {'Due Date':<12} {'Title'}")
    print("  " + "-" * 50)
    for task in pending:
        print(f"  {task['id']:<5} {task['due_date']:<12} {task['title']}")
        if task["description"]:
            print(f"  {'':5} {'':12} -> {task['description']}")


def handle_track_progress(tasks):
    """Handles the 'Track progress' menu option."""
    print("\n--- Progress Report ---")
    stats = task_utils.calculate_progress(tasks)

    bar_length = 30
    filled = int(bar_length * stats["percentage"] / 100)
    bar = "#" * filled + "-" * (bar_length - filled)

    print(f"\n  Total tasks  : {stats['total']}")
    print(f"  Completed    : {stats['completed']}")
    print(f"  Pending      : {stats['pending']}")
    print(f"  Progress     : [{bar}] {stats['percentage']}%")


def main():
    """
    Main program loop. Displays the menu, reads user input, validates the
    choice, and delegates to the appropriate handler function.
    """
    tasks = []  # In-memory task store: list of task dictionaries
    valid_choices = ["1", "2", "3", "4", "5", "6"]

    print("\nWelcome to the Task Management System!")

    while True:
        display_menu()
        choice = input("  Select an option (1-6): ").strip()

        is_valid, error = validation.validate_menu_choice(choice, valid_choices)
        if not is_valid:
            print(f"\n  [Error] {error}")
            continue

        if choice == "1":
            handle_add_task(tasks)
        elif choice == "2":
            handle_complete_task(tasks)
        elif choice == "3":
            handle_view_pending(tasks)
        elif choice == "4":
            print("\n--- All Tasks ---")
            task_utils.view_all_tasks(tasks)
        elif choice == "5":
            handle_track_progress(tasks)
        elif choice == "6":
            print("\n  Goodbye! Stay productive.\n")
            break


if __name__ == "__main__":
    main()
