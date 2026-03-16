"""
task_utils.py  (root shim)
This module has been moved into the task_manager package.
All names are re-exported from task_manager.task_utils for backward compatibility.
"""

from task_manager.task_utils import *  # noqa: F401, F403


# Internal counter used to assign unique IDs to new tasks.
_next_id = 1


def _get_next_id():
    """Returns and increments the internal task ID counter."""
    global _next_id
    task_id = _next_id
    _next_id += 1
    return task_id


def add_task(tasks, title, description="", due_date=""):
    """
    Validates inputs, creates a new task dictionary, and appends it to the
    tasks list.

    Args:
        tasks (list):       The current list of task dictionaries.
        title (str):        The title of the new task.
        description (str):  An optional description for the task.
        due_date (str):     An optional due date in YYYY-MM-DD format.

    Returns:
        dict: The newly created task dictionary.

    Raises:
        ValueError: If any input fails validation.
    """
    is_valid, error = validation.validate_task_title(title)
    if not is_valid:
        raise ValueError(f"Invalid title: {error}")

    is_valid, error = validation.validate_task_description(description)
    if not is_valid:
        raise ValueError(f"Invalid description: {error}")

    is_valid, error = validation.validate_due_date(due_date)
    if not is_valid:
        raise ValueError(f"Invalid due date: {error}")

    task = {
        "id": _get_next_id(),
        "title": title.strip(),
        "description": description.strip(),
        "due_date": due_date.strip(),
        "completed": False,
    }
    tasks.append(task)
    return task


def mark_task_as_complete(tasks, task_id):
    """
    Validates the task ID then marks the matching task as complete.

    Args:
        tasks (list):       The current list of task dictionaries.
        task_id (int|str):  The ID of the task to mark complete.

    Returns:
        True  if the task was found and updated.
        None  if the task was already complete.
        False if the task ID does not exist.

    Raises:
        ValueError: If task_id fails validation.
    """
    is_valid, error = validation.validate_task_id(task_id, tasks)
    if not is_valid:
        raise ValueError(f"Invalid task ID: {error}")

    task_id = int(task_id)
    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                return None  # Already complete — signal to caller
            task["completed"] = True
            return True
    return False


def view_pending_tasks(tasks):
    """
    Returns a list of all tasks that have not yet been completed.

    Args:
        tasks (list): The current list of task dictionaries.

    Returns:
        list: A filtered list containing only incomplete task dictionaries.
    """
    return [task for task in tasks if not task["completed"]]


def calculate_progress(tasks):
    """
    Calculates and returns progress statistics for the task list.

    Args:
        tasks (list): The current list of task dictionaries.

    Returns:
        dict: A dictionary with keys:
              - "total"      (int)   total number of tasks
              - "completed"  (int)   number of completed tasks
              - "pending"    (int)   number of pending tasks
              - "percentage" (float) completion percentage (0.0 – 100.0)
    """
    total = len(tasks)
    completed = sum(1 for task in tasks if task["completed"])
    pending = total - completed
    percentage = (completed / total * 100) if total > 0 else 0.0
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "percentage": round(percentage, 1),
    }


def view_all_tasks(tasks):
    """
    Prints a formatted table of all tasks regardless of status.

    Args:
        tasks (list): The current list of task dictionaries.
    """
    if not tasks:
        print("  No tasks found.")
        return

    print(f"\n  {'ID':<5} {'Done':<6} {'Due Date':<12} {'Title'}")
    print("  " + "-" * 60)
    for task in tasks:
        done_label = "Yes" if task["completed"] else "No"
        print(
            f"  {task['id']:<5} {done_label:<6} {task['due_date']:<12} {task['title']}"
        )
        if task["description"]:
            print(f"  {'':5} {'':6} {'':12} -> {task['description']}")
