# Level 8 -- Reflog recovery

Category: History
Completed: 2026-07-14

## Goal

Someone just ran `git reset --hard HEAD~1` on main -- the "Critical bug
fix" commit is no longer reachable from any branch or tag. Nothing is
actually deleted yet: git keeps a log of everywhere HEAD has pointed.

Use the reflog to find that commit, and get `main` pointing at it again.

## Reference command

```
git reflog                 # find the sha for 'Critical bug fix'
git reset --hard <that-sha>
```
