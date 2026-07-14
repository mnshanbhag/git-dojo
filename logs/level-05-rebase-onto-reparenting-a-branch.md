# Level 5 -- rebase --onto: reparenting a branch

Category: History
Completed: 2026-07-14

## Goal

`feature` was accidentally branched off `staging` instead of `main`, so
it carries staging's "Staging-only tweak" commit in its history -- a
commit that must never end up in feature or in main.

Reparent `feature` so it sits directly on top of `main`, keeping only its
own two commits ("Feature part 1", "Feature part 2"), with staging's
commit gone from its history entirely. Do it with a single rebase
command -- don't cherry-pick the commits by hand.

## Reference command

```
git rebase --onto main staging feature
```
