# Level 1 — Plumbing basics

Goal: see how a commit is actually stored — commit → tree → blob — using
plumbing commands instead of porcelain (`log`, `show`, `add`, `commit`).

## Commands & findings

**A commit object is just a pointer to a tree, plus metadata:**
```
$ git cat-file -t a3d0801
commit

$ git cat-file -p a3d0801
tree 54c54f6288a4fc2d3f76e8d33b55c55361fcec27
author mnshanbhag <mnshanbhag@gmail.com> 1783973140 +0100
committer mnshanbhag <mnshanbhag@gmail.com> 1783973140 +0100

Initial scaffold: toy CLI, README with 25-level curriculum tracker
```
No diff is stored anywhere — a commit is a snapshot (one tree) plus a
message and parent pointers (none here, it's the root commit).

**A tree object lists blobs (files) and other trees (subdirectories), each
by content hash and file mode:**
```
$ git cat-file -p 54c54f6
100644 blob 8a0e683a81c14d4fcb17816481413eeee7ffe462  .gitignore
100644 blob b11a90e518684d23933f2df0cd4df5ffaf0cdc9c  README.md
040000 tree 18c0873c83c808f7f0e05922a37fb4d5696556bc  logs
100644 blob e208428d370709070fa54125216adf860628e48e  pyproject.toml
040000 tree 9656418dace01e4fed7dd7ad0cb8bdbe5f7df65b  src
040000 tree 0f3ee14c87ec844225346ddec52a972d87d6f672  tests
```
Mode `100644` = regular file, `040000` = subdirectory (its own tree object).

**A blob is just the file's raw bytes, addressed by SHA-1 of its content:**
```
$ git cat-file -t b11a90e
blob
$ git cat-file -s b11a90e
2420
```

**Content addressing, proven directly:** `git hash-object` computes the
blob SHA a file *would* get without touching the index or working tree;
`-w` additionally writes it into `.git/objects` as a loose object.
```
$ echo -n "hello git-dojo" > sample.txt
$ git hash-object sample.txt
1d0b464299db3bc87e48563a76ba5d89693bbad0
$ git hash-object -w sample.txt
1d0b464299db3bc87e48563a76ba5d89693bbad0   # same hash, now written

$ find .git/objects -type f | grep 1d0b46
.git/objects/1d/0b464299db3bc87e48563a76ba5d89693bbad0
```
Objects are stored under `.git/objects/<first 2 chars>/<remaining 38 chars>`
of their SHA-1. This blob isn't referenced by any tree, so it's an
unreachable object — harmless, and eventually swept by `git gc`.

**`git ls-files -s` shows the index (staging area) itself, which is really
just a flat list of (mode, blob SHA, path) — the same shape a tree
collapses into:**
```
$ git ls-files -s
100644 8a0e683a81c14d4fcb17816481413eeee7ffe462 0  .gitignore
100644 b11a90e518684d23933f2df0cd4df5ffaf0cdc9c 0  README.md
...
```

## Takeaway

Porcelain commands (`add`, `commit`, `log`) are a UI over four object
types — blob, tree, commit, tag — all addressed by the SHA-1 of their
content. A commit never stores a diff; `git diff`/`log -p` compute diffs
on the fly by comparing two trees. This is the foundation for why
operations like rebase, cherry-pick, and reset are cheap and why identical
file content across commits/branches shares the same blob on disk.
