# Level 7 -- git bisect

Category: History
Completed: 2026-07-14

## Goal

calc.py's add() function used to work correctly. Somewhere along the way,
a commit disguised as an innocuous refactor silently broke it, and HEAD
is now bad.

check.py (present from the "Implement add()" commit onward) will tell you
pass/fail for any commit from that point on -- run `python check.py`
yourself, or let git drive the whole search with
`git bisect run python check.py`.

Known good: the "Implement add()" commit itself was fine.
Known bad: HEAD.

Find the exact commit that introduced the bug, write its full commit SHA
into answer.txt, and don't forget to `git bisect reset` when you're done.

## Reference command

```
git bisect start
git bisect bad HEAD
git bisect good <sha of 'Implement add()'>
git bisect run python check.py
echo <reported-sha> > answer.txt
git bisect reset
```
