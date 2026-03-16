"""
task_manager/task_utils.py
Core utility functions for managing tasks in the Task Management System.
Tasks are stored as a list of dictionaries with the following structure:
    {
        "id":          int   - unique task identifier,
        "title":       str   - task title,
        "description": str   - optional detailed description,
        "due_date":    str   - due date in YYYY-MM-DD format (optional),
        "completed":   bool  - True if task is complete, False if pending
    }
"""

from . import validation


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
    Validates all inputs, creates a new task dictionary, and appends it to
    the tasks list.

    Validation performed (via validation module):
        - tasks must be a list
        - title: non-empty string, max 100 chars
        - description: string, max 500 chars
        - due_date: empty or valid YYYY-MM-DD calendar date

    Args:
        tasks (list):       The current list of task dictionaries.
        title (str):        The title of the new task.
        description (str):  An optional description for the task.
        due_date (str):     An optional due date in YYYY-MM-DD format.

    Returns:
        dict: The newly created task dictionary.

    Raises:
        TypeError:  If tasks is not a list.
        ValueError: If any field fails validation.
    """
    if not isinstance(tasks, list):
        raise TypeError(
            f"tasks must be a list, got {type(tasks).__name__}."
        )

    is_valid, error = validation.validate_task_title(title)
    if not is_valid:
        raise ValueError(f"Invalid title — {error}")

    is_valid, error = validation.validate_task_description(description)
    if not is_valid:
        raise ValueError(f"Invalid description — {error}")

    is_valid, error = validation.validate_due_date(due_date)
    if not is_valid:
        raise ValueError(f"Invalid due date — {error}")

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

    Validation performed (via validation module):
        - task_id must be an integer that exists in tasks
        - the task's completed field is verified to be a bool before toggling

    Args:
        tasks (list):       The current list of task dictionaries.
        task_id (int|str):  The ID of the task to mark complete.

    Returns:
        True  if the task was found and updated.
        None  if the task was already complete.
        False if the task ID does not exist.

    Raises:
        ValueError: If task_id or the task's completed flag fails validation.
    """
    is_valid, error = validation.validate_task_id(task_id, tasks)
    if not is_valid:
        raise ValueError(f"Invalid task ID — {error}")

    task_id = int(task_id)
    for task in tasks:
        if task["id"] == task_id:
            is_valid, error = validation.validate_completed(task["completed"])
            if not is_valid:
                raise ValueError(
                    f"Task {task_id} has a corrupt 'completed' field — {error}"
                )
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
