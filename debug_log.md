# Debug Log: TaskMaster CLI

## Bug 1: [Describe what was broken]
- **Line(s):** [e.g., Line 13]
- **Error Message:** [Paste the exact error]
- **Root Cause:** [Why did it happen?]
- **Fix:** [What did you change?]

## Bug 1: **Return argument broken showing undefined error for sysntax """task.completed"""
- **Line(s):**
+ line 35

- **Error Message:** 
+ line 35, in list_tasks
+ status = "✓" if task.completed else "✗"
+                 ^^^^
+ NameError: name 'task' is not defined. Did you mean: 'tasks'?

- **Root Cause:**
+ task @ task.completed was not defined
+ ".completed" added unneccesory error
+ line 43, in complete_task
+    task.completed = True
+    ^^^^^^^^^^^^^^
+ AttributeError: 'dict' object has no attribute 'completed'

## Bug 2: 
**Line(s):**
+ 
