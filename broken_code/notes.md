# Debug Log: TaskMaster CLI

**Date:** 2026-08-14
**Source:** AI-generated `broken.py`, described as containing "5 hidden bugs and 2 logical errors."

## Bug 1: Dict accessed as an object attribute (`list_tasks`)
- **Line(s):** `status = "✓" if task.completed else "✗"`
- **Error Message:**
  ```
  status = "✓" if task.completed else "✗"
                  ^^^^
  NameError: name 'task' is not defined. Did you mean: 'tasks'?
  ```
  (This surfaces as a `NameError`/`AttributeError` depending on scope — the real issue is below.)
- **Root Cause:** Tasks are stored as dictionaries (`{"id": ..., "description": ..., "completed": ...}`), not objects. `task.completed` tries to access an attribute that doesn't exist on a dict.
- **Fix:** Changed to `task["completed"]`.

## Bug 2: Same dict-vs-attribute mistake in `complete_task`
- **Line(s):** `task.completed = True`
- **Error Message:** `AttributeError: 'dict' object has no attribute 'completed'`
- **Root Cause:** Same as Bug 1 ... attempting to set an attribute on a dict instead of assigning a key.
- **Fix:** Changed to `task["completed"] = True`.

## Bug 3: Unhandled `ValueError` in delete flow
- **Line(s):** `task_id = int(input("Enter task ID to delete: "))` (option 4, `main()`)
- **Error Message:** `ValueError: invalid literal for int() with base 10: '<non-numeric input>'`
- **Root Cause:** No `try/except` around the `int()` conversion at all ... any non-numeric input crashes the whole program instead of prompting again.
- **Fix:** Wrapped the input in a `try/except ValueError` inside a loop that re-prompts until a valid integer is entered, matching the pattern used for "complete task."

## Bug 4: Referencing `task_id` after a failed conversion (complete flow)
- **Line(s):** option 3 block in `main()`
- **Root Cause:** The original `try/except` printed an error message on bad input but still fell through to `complete_task(task_id)` afterward. If the `int()` call failed, `task_id` was never assigned, so this would raise an `UnboundLocalError` on the next line.
- **Fix:** Wrapped in a `while True` loop that only calls `complete_task(task_id)` once a valid integer has actually been assigned.

## Bug 5: No input sanitization on task descriptions
- **Line(s):** `desc = input("Enter task description: ")` (option 1)
- **Root Cause:** Raw input was stored as-is ... leading/trailing whitespace and inconsistent casing (`"buy milk"` vs `"Buy Milk"`) would be treated as different tasks even when the user meant the same thing.
- **Fix:** Changed to `input(...).strip().title()`.

---

## Known issue — NOT fixed yet

## Bug 6: Task IDs collide after deletion
- **Location:** `add_task()` — `new_id = len(tasks) + 1`
- **Root Cause:** New IDs are derived from the current *count* of tasks, not from the highest ID ever assigned. Example: add 3 tasks (IDs 1, 2, 3) → delete task 2 → list now has 2 tasks → add a new task → `new_id = len(tasks) + 1 = 3`, but ID 3 already exists. Two tasks now share the same ID.
- **Status:** Still present in `fixed.py`. This one wasn't caught this round ... worth revisiting.
- **Likely fix for next time:** Track IDs as `max(t["id"] for t in tasks) + 1 if tasks else 1`, or use a separate incrementing counter that never gets reused.

## Bug 7: Leftover dead code in `delete_task`
- **Location:** `new_id = len(tasks) - 1` inside `delete_task()`
- **Root Cause:** This line was added at some point but the variable is never used, it has no effect on the function's behavior. Likely a leftover from an earlier (incorrect) attempt to fix Bug 6 in the wrong place.
- **Fix:** Can be safely deleted; it's noise, not a fix.

---

## Summary

| # | Bug                                        | Type                   | Fixed?     |
|---|--------------------------------------------|------------------------|------------|
| 1 | `task.completed` in `list_tasks`           | AttributeError         | Done       |
| 2 | `task.completed = True` in `complete_task` | AttributeError         | Done       |
| 3 | No exception handling on delete input      | Unhandled crash        | Done       |
| 4 | `task_id` used after failed conversion     | UnboundLocalError risk | Done       |
| 5 | No input sanitization on descriptions      | Data consistency       | Done       |
| 6 | ID collision after deletion                | Logical error          | still open |
| 7 | Dead `new_id` variable in `delete_task`    | Code cleanliness       | still open |

## Skills exercised

Dict vs. object access, exception handling around user input, control-flow bugs (using a variable that may never get assigned), and one logical/data-integrity bug that slipped through ... a good reminder that "it runs without crashing" isn't the same as "it's correct."
