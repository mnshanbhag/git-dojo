# Level 6 -- Splitting a commit

Category: History
Completed: 2026-07-14

## Goal

The tip commit ("Add utils and config") bundles two unrelated additions:
utils.py and config.py. Split it into two commits, in this order:
1. "Add utils" -- containing only utils.py
2. "Add config" -- containing only config.py

Use interactive rebase to pause on that commit and edit it, rather than
just resetting the branch and starting over.

## Reference command

```
git rebase -i HEAD~1      # change 'pick' to 'edit' for the commit
git reset HEAD^
git add utils.py && git commit -m "Add utils"
git add config.py && git commit -m "Add config"
git rebase --continue
```
