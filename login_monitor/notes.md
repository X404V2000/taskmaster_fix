# Debug Log: Login Monitor

**Date:** 2026-08-21
**Goal:** Flag any IP with 3+ failed login attempts from a parsed log.

## Bug 1: String compared to boolean (`count_failures`)
- **Line(s):** `if attempt["ip"] == ip and attempt["success"] == False:`
- **Root Cause:** `parse_attempts` splits raw CSV lines, so `success` is always a *string* (`"True"` / `"False"`), never a Python boolean. Comparing a string to the boolean `False` is always `False`, so every failure count silently came back as `0`.
- **Fix:** Compare to the string instead ... `attempt["success"] == "False"`.
- **This was the main bug** ... everything downstream (alerts, summary count) was wrong because of it.

## Bug 2: Off-by-one on the threshold (`flag_suspicious`)
- **Line(s):** `if fail_count > threshold:`
- **Root Cause:** With `threshold = 3`, `>` requires *more than* 3 failures (4+) to trigger an alert. The spec says "3 or more."
- **Fix:** Changed to `>=`.

## Bug 3: Mutable default argument (`build_alert`)
- **Line(s):** `def build_alert(ip, count: int, tags={}) -> Dict:`
- **Root Cause:** Default argument values in Python are created *once*, when the function is defined ... not fresh on every call. Using a mutable `{}` as a default means every call that doesn't pass `tags` explicitly shares and mutates the *same* dictionary. In a loop calling `build_alert` multiple times, this silently leaks data between calls.
- **Fix:** `tags: Dict = None`, then `if tags is None: tags = {}` inside the function body ... a fresh dict every call.

## Bug 4: Silent exception swallowing (`main`)
- **Line(s):** `except Exception: pass`
- **Root Cause:** Catches every possible error and does nothing ... if any of the above bugs had raised an exception instead of failing silently, this would have hidden it completely, making debugging much harder.
- **Fix:** `except Exception as e: print(f"Error: {e}")` ... errors are now visible.

## Refactor (not a bug, but done alongside the fixes)
`count_failures` was rewritten from an O(n²) approach (re-scanning the full attempt list once per unique IP inside `flag_suspicious`) into a single-pass version using `collections.defaultdict`, returning failure counts for every IP at once. Cleaner and faster on larger logs.

---

## Corrections to my first pass at these notes

My initial read misdiagnosed a few things ... worth recording so I don't repeat the same misreads:

- I flagged `parse_attempts`'s parameter as "missing/undefined." It wasn't ... `log_lines` was a properly defined parameter, just renamed to `raw_log` in the fixed version. That rename fixed nothing; I was looking at the wrong function for the real bug (Bug 1, above, was actually in `count_failures`).
- I flagged `attempts` and `ip` in `count_failures` as "not defined." They were defined correctly as parameters ... the actual problem was the `== False` comparison, not missing variables.
- I flagged `tags` in `build_alert` as "not defined." It was defined (via the `{}` default) ... the real problem was that it was a *mutable* default shared across calls, which is a much less obvious bug than "undefined."
- My original fix list only documented the `count_failures` refactor. It didn't record that I'd also fixed the string/boolean comparison, the `>`/`>=` threshold bug, or the bare `except: pass` ... all three were fixed in the code but never written up.

Lesson: name the actual mechanism of the bug (type mismatch, off-by-one, mutable default, silent exception) rather than a vague "not defined" ... it's more accurate and it's what actually helps when reviewing this later.

## Summary

| # | Bug                                   | Type                  | Fixed? |
|---|---------------------------------------|-----------------------|--------|
| 1 | `success == False` (string vs bool)   | Type/comparison error | Done   |
| 2 | `>` instead of `>=` on threshold      | Off-by-one            | Done   |
| 3 | Mutable default arg in `build_alert`  | Classic Python trap   | Done   |
| 4 | Bare `except: pass`                   | Silent failure        | Done   |
