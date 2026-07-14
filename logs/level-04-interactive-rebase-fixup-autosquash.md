# Level 4 -- Interactive rebase: fixup + autosquash

Category: History
Completed: 2026-07-14

## Goal

app.py has a bug: login() returns "Ok" but should return "OK" (all caps).
There's only one commit, "Add login feature", which introduced the bug.

Fix the bug, but don't make a normal commit for it. Instead, commit the
fix as a *fixup* commit targeting the buggy commit, then use interactive
rebase with autosquash to fold it back in automatically. When you're
done there should be exactly one commit, still titled "Add login
feature", with the bug fixed.

(To run autosquash without an editor popping up, set GIT_SEQUENCE_EDITOR
to a no-op, e.g. `true`, before the rebase command.)

## Reference command

```
git add app.py
git commit --fixup HEAD
GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash --root
```
