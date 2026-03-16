"""
task_manager/validation.py
Input validation functions for the Task Management System.

Every public function returns a (bool, str) tuple:
    (True,  "")           – input is valid
    (False, "<message>")  – input is invalid; message describes the problem
"""

import re
from datetime import date as _date


def validate_task_title(title):
    """
    Validates that a task title is a non-empty string within the allowed length.

    Rules:
        - Must be a str
        - Must not be blank after stripping whitespace
        - Must be 1–100 characters (after stripping)

    Args:
        title: The value to validate.

    Returns:
        tuple: (bool, str)
    """
    if not isinstance(title, str):
        return False, (
            f"Title must be a string, got {type(title).__name__}."
        )
    stripped = title.strip()
    if len(stripped) == 0:
        return False, "Title cannot be empty or contain only whitespace."
    if len(stripped) > 100:
        return False, (
            f"Title is too long ({len(stripped)} chars). Maximum is 100 characters."
        )
    return True, ""


def validate_task_description(description):
    """
    Validates a task description.

    Rules:
        - Must be a str
        - May be empty
        - Must not exceed 500 characters

    Args:
        description: The value to validate.

    Returns:
        tuple: (bool, str)
    """
    if not isinstance(description, str):
        return False, (
            f"Description must be a string, got {type(description).__name__}."
        )
    if len(description) > 500:
        return False, (
            f"Description is too long ({len(description)} chars). "
            "Maximum is 500 characters."
        )
    return True, ""


def validate_due_date(due_date):
    """
    Validates that a due date is empty (optional) or a real YYYY-MM-DD date.

    Rules:
        - Must be a str
        - May be empty / whitespace-only (field is optional)
        - Must match YYYY-MM-DD format exactly
        - The date values must form a valid calendar date

    Args:
        due_date: The value to validate.

    Returns:
        tuple: (bool, str)
    """
    if not isinstance(due_date, str):
        return False, (
            f"Due date must be a string, got {type(due_date).__name__}."
        )
    stripped = due_date.strip()
    if stripped == "":
        return True, ""  # field is optional
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", stripped):
        return False, (
            f"Due date '{stripped}' is not in the required YYYY-MM-DD format "
            "(e.g. 2024-06-26)."
        )
    try:
        year, month, day = (int(p) for p in stripped.split("-"))
        _date(year, month, day)
    except ValueError:
        return False, (
            f"Due date '{stripped}' is not a valid calendar date."
        )
    return True, ""


def validate_completed(completed):
    """
    Validates that a completed flag is a boolean.

    Rules:
        - Must be exactly True or False (not just truthy/falsy)

    Args:
        completed: The value to validate.

    Returns:
        tuple: (bool, str)
    """
    if not isinstance(completed, bool):
        return False, (
            f"Completed flag must be True or False, "
            f"got {type(completed).__name__} (value: {completed!r})."
        )
    return True, ""


def validate_menu_choice(choice, valid_options):
    """
    Validates that the user's menu choice is among the accepted options.

    Args:
        choice (str):         The user's raw input.
        valid_options (list): Accepted option strings.

    Returns:
        tuple: (bool, str)
    """
    if choice not in valid_options:
        options_str = ", ".join(valid_options)
        return False, (
            f"'{choice}' is not a valid option. Please enter one of: {options_str}."
        )
    return True, ""


def validate_task_id(task_id, tasks):
    """
    Validates that a task ID is a whole number that exists in the task list.

    Args:
        task_id (str | int): The ID supplied by the user.
        tasks (list):        The current list of task dictionaries.

    Returns:
        tuple: (bool, str)
    """
    # Reject floats explicitly — int(1.5) truncates to 1 without raising,
    # which would silently match an existing task ID.
    if isinstance(task_id, float):
        return False, f"Task ID must be a whole number, got {task_id!r}."
    try:
        task_id = int(task_id)
    except (ValueError, TypeError):
        return False, f"Task ID must be a whole number, got {task_id!r}."
    if not tasks:
        return False, "There are no tasks yet — add a task first."
    task_ids = [task["id"] for task in tasks]
    if task_id not in task_ids:
        if len(task_ids) <= 8:
            return False, (
                f"No task found with ID {task_id}. "
                f"Available ID(s): {task_ids}."
            )
        return False, (
            f"No task found with ID {task_id}. "
            f"There are {len(task_ids)} tasks — check the task list for valid IDs."
        )
    return True, ""
