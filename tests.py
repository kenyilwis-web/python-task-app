"""
tests.py
Comprehensive test suite for the Task Management System.

Run from the project root (same directory as main.py):
    python tests.py
"""

import sys
import traceback

# Ensure the package is importable from the project root.
sys.path.insert(0, ".")
from task_manager import validation, task_utils  # noqa: E402

# ── Helpers ───────────────────────────────────────────────────────────────────

PASS = "[PASS]"
FAIL = "[FAIL]"
_results = {"passed": 0, "failed": 0}

def _assert(condition, message):
      """Raise AssertionError with message if condition is False."""
      if not condition:
            raise AssertionError(message)
      return condition




def check(label, result_tuple, expect_valid, msg_fragment=""):
    """
    Asserts a (bool, str) validation result matches expectations.

    Args:
        label (str):          Human-readable test description.
        result_tuple (tuple): (bool, str) from a validator.
        expect_valid (bool):  Expected validity flag.
        msg_fragment (str):   Optional substring that must appear (case-insensitive)
                              in the error message when expect_valid is False.
    """
    got_valid, got_msg = result_tuple
    fragment_ok = (
        msg_fragment == ""
        or msg_fragment.lower() in got_msg.lower()
    )
    ok = got_valid == expect_valid and fragment_ok

    _results["passed" if ok else "failed"] += 1
    print(f"  {PASS if ok else FAIL}  {label}")
    if not ok:
        if got_valid != expect_valid:
            print(f"         expected valid={expect_valid}, got valid={got_valid}")
        if not fragment_ok:
            print(f"         expected msg containing {msg_fragment!r}")
            print(f"         got msg: {got_msg!r}")


def section(title):
    print(f"\n{'=' * 55}")
    print(f"  {title}")
    print(f"{'=' * 55}")


# ── validate_task_title ───────────────────────────────────────────────────────

section("validate_task_title")

check("normal title",
      validation.validate_task_title("Buy milk"),
      True)

check("leading/trailing whitespace (stripped, valid)",
      validation.validate_task_title("  Buy milk  "),
      True)

check("exactly 100 chars (boundary ok)",
      validation.validate_task_title("a" * 100),
      True)

check("101 chars (one over limit)",
      validation.validate_task_title("a" * 101),
      False, "101")

check("empty string",
      validation.validate_task_title(""),
      False, "empty")

check("whitespace only",
      validation.validate_task_title("   "),
      False, "empty")

check("non-string: int",
      validation.validate_task_title(123),
      False, "string")

check("non-string: None",
      validation.validate_task_title(None),
      False, "string")

check("non-string: list",
      validation.validate_task_title(["Buy milk"]),
      False, "string")

# ── validate_task_description ─────────────────────────────────────────────────

section("validate_task_description")

check("empty string (allowed)",
      validation.validate_task_description(""),
      True)

check("normal description",
      validation.validate_task_description("Shop at Market Basket for food"),
      True)

check("exactly 500 chars (boundary ok)",
      validation.validate_task_description("x" * 500),
      True)

check("501 chars (one over limit)",
      validation.validate_task_description("x" * 501),
      False, "501")

check("non-string: int",
      validation.validate_task_description(42),
      False, "string")

check("non-string: None",
      validation.validate_task_description(None),
      False, "string")

check("non-string: list",
      validation.validate_task_description([]),
      False, "string")

# ── validate_due_date ─────────────────────────────────────────────────────────

section("validate_due_date")

check("empty string (optional field ok)",
      validation.validate_due_date(""),
      True)

check("whitespace only (treated as empty, ok)",
      validation.validate_due_date("   "),
      True)

check("valid date 2024-06-26",
      validation.validate_due_date("2024-06-26"),
      True)

check("valid date 2000-01-01",
      validation.validate_due_date("2000-01-01"),
      True)

check("valid leap day 2024-02-29",
      validation.validate_due_date("2024-02-29"),
      True)

check("invalid leap day 2023-02-29 (non-leap year)",
      validation.validate_due_date("2023-02-29"),
      False, "valid calendar")

check("wrong format DD-MM-YYYY",
      validation.validate_due_date("26-06-2024"),
      False, "yyyy-mm-dd")

check("wrong format MM/DD/YYYY",
      validation.validate_due_date("06/26/2024"),
      False, "yyyy-mm-dd")

check("partial date YYYY-MM",
      validation.validate_due_date("2024-06"),
      False, "yyyy-mm-dd")

check("impossible month 2024-13-01",
      validation.validate_due_date("2024-13-01"),
      False, "valid calendar")

check("impossible day 2024-02-30",
      validation.validate_due_date("2024-02-30"),
      False, "valid calendar")

check("impossible day 2024-04-31 (April has 30 days)",
      validation.validate_due_date("2024-04-31"),
      False, "valid calendar")

check("all zeros 0000-00-00",
      validation.validate_due_date("0000-00-00"),
      False, "valid calendar")

check("non-string: int",
      validation.validate_due_date(20240626),
      False, "string")

check("non-string: None",
      validation.validate_due_date(None),
      False, "string")

# ── validate_completed ────────────────────────────────────────────────────────

section("validate_completed")

check("True",
      validation.validate_completed(True),
      True)

check("False",
      validation.validate_completed(False),
      True)

check("integer 1 (truthy but not bool)",
      validation.validate_completed(1),
      False, "true or false")

check("integer 0 (falsy but not bool)",
      validation.validate_completed(0),
      False, "true or false")

check("None",
      validation.validate_completed(None),
      False, "true or false")

check('string "true"',
      validation.validate_completed("true"),
      False, "true or false")

check('string "false"',
      validation.validate_completed("false"),
      False, "true or false")

# ── validate_menu_choice ──────────────────────────────────────────────────────

section("validate_menu_choice")

opts = ["1", "2", "3", "4", "5", "6"]

check("valid choice '1'",
      validation.validate_menu_choice("1", opts),
      True)

check("valid choice '6'",
      validation.validate_menu_choice("6", opts),
      True)

check("invalid choice '9'",
      validation.validate_menu_choice("9", opts),
      False, "'9'")

check("invalid choice '0'",
      validation.validate_menu_choice("0", opts),
      False)

check("empty string",
      validation.validate_menu_choice("", opts),
      False)

check("lowercase letter 'a'",
      validation.validate_menu_choice("a", opts),
      False)

check("choice with surrounding spaces ' 1 '",
      validation.validate_menu_choice(" 1 ", opts),
      False)

# ── validate_task_id ──────────────────────────────────────────────────────────

section("validate_task_id")

_id_tasks = [
    {"id": 1, "title": "T1", "description": "", "due_date": "", "completed": False},
    {"id": 2, "title": "T2", "description": "", "due_date": "", "completed": False},
]

check("valid id as int",
      validation.validate_task_id(1, _id_tasks),
      True)

check("valid id as string",
      validation.validate_task_id("2", _id_tasks),
      True)

check("missing id 99",
      validation.validate_task_id(99, _id_tasks),
      False, "no task found")

check("non-numeric string 'abc'",
      validation.validate_task_id("abc", _id_tasks),
      False, "whole number")

check("float string '1.5' (no truncation)",
      validation.validate_task_id("1.5", _id_tasks),
      False, "whole number")

check("float 1.5 (silent-truncation bug — must be caught)",
      validation.validate_task_id(1.5, _id_tasks),
      False, "whole number")

check("negative id -1",
      validation.validate_task_id(-1, _id_tasks),
      False, "no task found")

check("empty task list returns helpful message",
      validation.validate_task_id(1, []),
      False, "no tasks yet")

# ── add_task (integration) ────────────────────────────────────────────────────

section("add_task — integration")


def integration(label, fn, expect_exc=None):
    """Run fn() and check whether the expected exception is raised."""
    try:
        result = fn()
        if expect_exc is None:
            _results["passed"] += 1
            print(f"  {PASS}  {label} → {result}")
        else:
            _results["failed"] += 1
            print(f"  {FAIL}  {label} — expected {expect_exc.__name__}, got no exception")
    except Exception as exc:
        if expect_exc and isinstance(exc, expect_exc):
            _results["passed"] += 1
            print(f"  {PASS}  {label} → {type(exc).__name__}: {exc}")
        else:
            _results["failed"] += 1
            print(f"  {FAIL}  {label} — unexpected {type(exc).__name__}: {exc}")
            traceback.print_exc()


tasks = []

integration("valid task (no date)",
            lambda: task_utils.add_task(tasks, "Buy milk", "at the store", ""))

integration("valid task (with date)",
            lambda: task_utils.add_task(tasks, "Exercise", "", "2024-07-01"))

integration("whitespace title stripped → stored cleanly",
            lambda: task_utils.add_task(tasks, "  Groceries  ", "  Eggs  ", ""))

integration("empty title raises ValueError",
            lambda: task_utils.add_task(tasks, "", "desc", ""),
            ValueError)

integration("whitespace-only title raises ValueError",
            lambda: task_utils.add_task(tasks, "   ", "desc", ""),
            ValueError)

integration("description > 500 chars raises ValueError",
            lambda: task_utils.add_task(tasks, "T", "x" * 501, ""),
            ValueError)

integration("bad date format raises ValueError",
            lambda: task_utils.add_task(tasks, "T", "", "26-06-2024"),
            ValueError)

integration("invalid calendar date raises ValueError",
            lambda: task_utils.add_task(tasks, "T", "", "2024-02-30"),
            ValueError)

integration("non-list tasks raises TypeError",
            lambda: task_utils.add_task("not-a-list", "T", "", ""),
            TypeError)

# Verify actual field values
_t = [t for t in tasks if t["title"] == "Groceries"]
assert _t, "Stripped 'Groceries' task not found"
assert _t[0]["description"] == "Eggs", f"description not stripped: {_t[0]['description']!r}"
assert _t[0]["completed"] is False, "completed should default to False"
assert isinstance(_t[0]["id"], int), "id should be an int"
print(f"  {PASS}  whitespace stripped in stored task fields")
_results["passed"] += 1

# ── mark_task_as_complete (integration) ───────────────────────────────────────

section("mark_task_as_complete — integration")

_mc_tasks = []
_a = task_utils.add_task(_mc_tasks, "Task Alpha", "", "")
_b = task_utils.add_task(_mc_tasks, "Task Beta", "", "")

integration("first completion returns True",
            lambda: _assert(task_utils.mark_task_as_complete(_mc_tasks, _a["id"]) is True,
                            "expected True"))

integration("second completion returns None (idempotent)",
            lambda: _assert(task_utils.mark_task_as_complete(_mc_tasks, _a["id"]) is None,
                            "expected None"))

integration("missing id raises ValueError",
            lambda: task_utils.mark_task_as_complete(_mc_tasks, 9999),
            ValueError)

integration("float id raises ValueError",
            lambda: task_utils.mark_task_as_complete(_mc_tasks, 1.5),
            ValueError)

# ── view_pending_tasks ────────────────────────────────────────────────────────

section("view_pending_tasks")

_prog_tasks = []
task_utils.add_task(_prog_tasks, "Alpha", "", "")
task_utils.add_task(_prog_tasks, "Beta",  "", "")
task_utils.add_task(_prog_tasks, "Gamma", "", "")
task_utils.mark_task_as_complete(_prog_tasks, _prog_tasks[0]["id"])

pending = task_utils.view_pending_tasks(_prog_tasks)
_ok = len(pending) == 2 and all(not t["completed"] for t in pending)
_results["passed" if _ok else "failed"] += 1
print(f"  {PASS if _ok else FAIL}  returns 2 pending from 3 total "
      f"(got {len(pending)})")

pending_empty = task_utils.view_pending_tasks([])
_ok2 = pending_empty == []
_results["passed" if _ok2 else "failed"] += 1
print(f"  {PASS if _ok2 else FAIL}  empty list returns []")

# ── calculate_progress ────────────────────────────────────────────────────────

section("calculate_progress")


def prog_check(label, tasks_arg, expected):
    result = task_utils.calculate_progress(tasks_arg)
    ok = all(result[k] == v for k, v in expected.items())
    _results["passed" if ok else "failed"] += 1
    print(f"  {PASS if ok else FAIL}  {label}")
    if not ok:
        for k, v in expected.items():
            if result[k] != v:
                print(f"         {k}: expected {v!r}, got {result[k]!r}")


prog_check("empty list → 0% progress",
           [],
           {"total": 0, "completed": 0, "pending": 0, "percentage": 0.0})

prog_check("1 of 3 done → 33.3%",
           _prog_tasks,
           {"total": 3, "completed": 1, "pending": 2, "percentage": 33.3})

_all_done = []
task_utils.add_task(_all_done, "X", "", "")
task_utils.mark_task_as_complete(_all_done, _all_done[0]["id"])
prog_check("1 of 1 done → 100%",
           _all_done,
           {"total": 1, "completed": 1, "pending": 0, "percentage": 100.0})

# ── Summary ───────────────────────────────────────────────────────────────────

total = _results["passed"] + _results["failed"]
print(f"\n{'=' * 55}")
print(f"  Results: {_results['passed']}/{total} passed"
      f"  ({_results['failed']} failed)")
print(f"{'=' * 55}\n")

if _results["failed"] > 0:
    sys.exit(1)


# ── Internal helpers (defined after use to keep test output clean) ────────────

