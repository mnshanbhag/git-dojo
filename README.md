# git-dojo

An interactive trainer for advanced Git/GitHub techniques. It gives you a
goal, you run the real git command yourself in a disposable sandbox, and
`gitdojo check` verifies the result against that goal.

- 3 failed attempts → a nudge (an escalating hint, not the answer)
- Only a level you actually solved gets logged — the sandbox and your
  failed attempts are never recorded anywhere

## Setup

```
python -m venv .venv
.venv/Scripts/activate      # or: source .venv/bin/activate
pip install -e .
```

## Usage

```
gitdojo start 1     # sets up sandbox/ for level 1, prints the goal
cd sandbox
# ... run the real git command(s) yourself ...
cd ..
gitdojo check       # verifies sandbox/ against the goal
gitdojo hint        # show the current hint on demand, if you don't want to wait
gitdojo status      # see progress across all levels
```

On success, `gitdojo check` records the level as complete: it writes
`logs/level-NN-*.md` (goal + reference command) and flips the row below to
done. That's the only thing that gets tracked — no scratch work, no failed
attempts, no sandbox contents.

Levels 23-25 are the exception: branch protection, Actions, and releases
only mean anything server-side, so they run against a real disposable
GitHub repo (`git-dojo-gh-practice`) instead of a purely local sandbox.
`gitdojo check` only ever *reads* that repo's state via `gh` — it never
configures branch protection itself, since that's an access-control
change; you do that part yourself (through the GitHub UI or your own
`gh api` calls), same as every other level's "you run the command, we
verify it" model.

## Curriculum

Only levels with an entry in `src/gitdojo/levels/` are playable so far;
the rest of the table is the plan — implemented incrementally as we go,
since some (GitHub platform features especially) need their own checkers.

| # | Level | Category | Status | Log |
|---|-------|----------|--------|-----|
| 1 | Plumbing basics (`cat-file`, `hash-object`, `ls-tree`, `ls-files`) | Internals | ✅ | [log](logs/level-01-plumbing-basics-content-addressing.md) |
| 2 | Diff & blame mastery (diff algorithms, `--word-diff`, `blame --ignore-revs`) | Internals | ✅ | [log](logs/level-02-diff-blame-mastery-blame-ignore-rev.md) |
| 3 | `git notes` | Internals | ✅ | [log](logs/level-03-git-notes.md) |
| 4 | Interactive rebase (squash/fixup/autosquash/edit/reorder) | History | ✅ | [log](logs/level-04-interactive-rebase-fixup-autosquash.md) |
| 5 | `rebase --onto` | History | ✅ | [log](logs/level-05-rebase-onto-reparenting-a-branch.md) |
| 6 | Splitting a commit (`reset -p` / rebase `edit`) | History | ✅ | [log](logs/level-06-splitting-a-commit.md) |
| 7 | `git bisect` (manual + `bisect run`) | History | ✅ | [log](logs/level-07-git-bisect.md) |
| 8 | Reflog recovery | History | ✅ | [log](logs/level-08-reflog-recovery.md) |
| 9 | `rerere` (recorded conflict resolution) | History | ⬜ | |
| 10 | Cherry-pick backport | Branching | ⬜ | |
| 11 | Merge strategies (`-X ours`/`theirs`, octopus merge) | Branching | ⬜ | |
| 12 | Worktrees | Branching | ⬜ | |
| 13 | Submodule vs subtree | Branching | ⬜ | |
| 14 | Advanced stash (`-p`, to-branch, multiple) | Branching | ⬜ | |
| 15 | Hooks (`commit-msg`) | Config | ⬜ | |
| 16 | `.gitattributes` (union merge driver) | Config | ⬜ | |
| 17 | Git LFS | Config | ⬜ | |
| 18 | Signing (SSH commits & tags + verify) | Config | ⬜ | |
| 19 | Conditional config (`includeIf`) | Config | ⬜ | |
| 20 | Sparse-checkout + shallow/partial clone | Exchange | ⬜ | |
| 21 | `format-patch` / `git am` | Exchange | ⬜ | |
| 22 | `git bundle` / `git archive` | Exchange | ⬜ | |
| 23 | Branch protection + CODEOWNERS + required status checks | GitHub | ⬜ | |
| 24 | GitHub Actions: matrix builds | GitHub | ⬜ | |
| 25 | Release engineering: semver tag + release notes | GitHub | ⬜ | |

Status legend: ⬜ not started · ✅ done
