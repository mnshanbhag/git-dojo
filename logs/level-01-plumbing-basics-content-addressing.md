# Level 1 -- Plumbing basics: content-addressing

Category: Internals
Completed: 2026-07-14

## Goal

There's a file called mystery.txt in this sandbox. Without opening it in
an editor, use a git plumbing command to compute its git object SHA-1, and
write *just* that 40-character SHA (nothing else) into a new file called
answer.txt, in this same directory.

## Reference command

```
git hash-object mystery.txt > answer.txt
```
