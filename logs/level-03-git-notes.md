# Level 3 -- git notes

Category: Internals
Completed: 2026-07-14

## Goal

This repo has exactly one commit. Attach a git note to it with the exact
text "reviewed-by: alice" -- without amending the commit, and without creating
any new commit on top of it. (Notes live outside the normal commit
history, in their own ref.)

## Reference command

```
git notes add -m "reviewed-by: alice" HEAD
```
