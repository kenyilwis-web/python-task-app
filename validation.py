"""
validation.py  (root shim)
This module has been moved into the task_manager package.
All names are re-exported from task_manager.validation for backward compatibility.
"""

from task_manager.validation import *  # noqa: F401, F403


def validate_task_title(title):
    """
    Validates that a task title is a non-empty string within the allowed length.

    Args:
        title (str): The task title to validate.

    Returns:
        tuple: (bool, str) where bool indicates validity and str is an error
               message (empty string if valid).
    """
    if not isinstance(title, str):
        return False, "Title must be a string."
    title = title.strip()
    if len(title) == 0:
        return False, "Title cannot be empty."
    if len(title) > 100:
        return False, "Title cannot exceed 100 characters."
    return True, ""


def validate_task_description(description):
    """
    Validates that a task description is a string within the allowed length.
    An empty description is allowed.

    Args:
        description (str): The task description to validate.

    Returns:
        tuple: (bool, str) where bool indicates validity and str is an error
               message (empty string if valid).
    """
    if not isinstance(description, str):
        return False, "Description must be a string."
    if len(description) > 500:
        return False, "Description cannot exceed 500 characters."
    return True, ""


def validate_menu_choice(choice, valid_options):
    """
    Validates that the user's menu choice is one of the accepted options.

    Args:
        choice (str): The user's input choice.
        valid_options (list): A list of valid option strings.

    Returns:
        tuple: (bool, str) where bool indicates validity and str is an error
               message (empty string if valid).
    """
    if choice not in valid_options:
        options_str = ", ".join(valid_options)
        return False, f"Invalid choice. Please enter one of: {options_str}."
    return True, ""


def validate_due_date(due_date):
    """
    Validates that a due date is either empty or a valid YYYY-MM-DD calendar date.

    Args:
        due_date (str): The due date string to validate.

    Returns:
        tuple: (bool, str) where bool indicates validity and str is an error
               message (empty string if valid).
    """
    if not isinstance(due_date, str):
        return False, "Due date must be a string."
    due_date = due_date.strip()
    if due_date == "":
        return True, ""  # field is optional
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", due_date):
        return False, "Due date must be in YYYY-MM-DD format (e.g. 2024-06-26)."
    try:
        from datetime import date
        year, month, day = (int(p) for p in due_date.split("-"))
        date(year, month, day)
    except ValueError:
        return False, "Due date is not a valid calendar date."
    return True, ""


def validate_task_id(task_id, tasks):
    """
    Validates that a task ID exists within the current task list.

    Args:
        task_id (str | int): The task ID provided by the user.
        tasks (list): The current list of task dictionaries.

    Returns:
        tuple: (bool, str) where bool indicates validity and str is an error
               message (empty string if valid).
    """
    try:
        task_id = int(task_id)
    except (ValueError, TypeError):
        return False, "Task ID must be a whole number."

    task_ids = [task["id"] for task in tasks]
    if task_id not in task_ids:
        return False, f"No task found with ID {task_id}."
    return True, ""
