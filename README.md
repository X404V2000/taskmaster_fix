# taskmaster_fix

Weekly debugging practice: I ask an AI to generate realistic, working code with deliberately planted bugs, then fix it without being told what's wrong.

## Why this repo exists

Writing code with AI assistance is a given skill now. Being able to read, understand, and fix code you didn't write — especially when it's broken in non-obvious ways — is a different skill, and it's the one that actually matters on the job. This repo is where I build that muscle on purpose, every week.

## How it works

1. Prompt an AI to generate a small, realistic script (not a toy example) with 2-5 bugs planted in it — the code should run, or mostly run, but produce wrong results or fail in subtle ways.
2. Fix the bugs without hints, working only from the expected behavior.
3. Document what was actually wrong and what I changed.
4. Where relevant, improve the code beyond just fixing the bug (better structure, better performance, better error handling).

## Bug categories I practice against

- Logic errors that don't crash but produce silently wrong output (the hardest kind to catch)
- Type/comparison mistakes (e.g. comparing a string to a boolean)
- Off-by-one and boundary errors
- Mutable default argument bugs
- Poor exception handling (swallowed errors, overly broad `except`)
- Inefficient implementations that work but don't scale

## Structure

Each week gets its own folder or clearly named file pair:

```
YYYY-MM-DD_<topic>/
  broken.py       # the AI-generated version with bugs
  fixed.py        # my corrected version
  notes.md        # what was wrong, what I changed, what I learned
```

## Example: Login Attempt Monitor (2026-08-21)

A script meant to flag IP addresses with 3+ failed login attempts from a parsed log. It ran without crashing but silently produced wrong results.

**Bugs found and fixed:**
- Comparing a value to the Python boolean `False` instead of the string `"False"` it actually held after parsing — caused every failure count to come back as zero.
- Used `>` instead of `>=` against the threshold, so IPs at exactly the threshold weren't flagged.
- A function used a mutable dict (`{}`) as a default argument, which persists across calls instead of resetting — a classic Python trap.
- A broad `except Exception: pass` was silently hiding all of the above instead of surfacing the real error.

**Also improved:** rewrote the failure-counting logic from an O(n²) approach (re-scanning the full log for every IP) into a single pass using `collections.defaultdict`.

## Skills this is building toward

Data engineering and backend development — specifically the ability to work with real-world data pipelines and systems where "the code runs" isn't the same as "the code is correct." Debugging discipline transfers directly to production data work, where silent, wrong-output bugs are far more dangerous than crashes.

## About me

Bachelor of Information Science student (UNISA), self-teaching Linux, SQL, Python, and computer architecture toward a data engineering / backend engineering career.
