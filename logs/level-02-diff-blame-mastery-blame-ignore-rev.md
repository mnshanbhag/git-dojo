# Level 2 -- Diff & blame mastery: blame --ignore-rev

Category: Internals
Completed: 2026-07-14

## Goal

poem.txt has three lines. The first two were written in one commit, then
a later commit reformatted the whole file (added leading indentation to
every line) without changing its meaning. A third line was then added
normally.

Plain `git blame poem.txt` blames that reformat commit for lines 1 and 2,
which is useless -- it wasn't the reformat commit that actually wrote
that text. Find out which commit *really* introduced line 1 ("roses are
red"), by having blame skip over the reformat commit, and write that
commit's SHA (full or abbreviated, at least 7 characters) into answer.txt.

## Reference command

```
git log --oneline -- poem.txt   # find the reformat commit's SHA
git blame --ignore-rev <reformat-sha> poem.txt   # read line 1's real SHA
echo <that-sha> > answer.txt
```
