# git-dojo

A learning project. The code here is a small, disposable toy CLI (a
quote-printing tool) — it exists only as a vehicle to practice advanced Git
and GitHub techniques. **What matters is this README and the history/PRs
behind it, not the app itself.**

Each level below is done on its own branch, merged via its own PR, and
logged in [`logs/`](logs/) with the commands used and what was learned.

## Progress

| # | Level | Category | Status | Log |
|---|-------|----------|--------|-----|
| 1 | Plumbing basics (`cat-file`, `hash-object`, `ls-tree`, `ls-files`) | Internals | ✅ | [log](logs/level-01-plumbing-basics.md) |
| 2 | Diff & blame mastery (diff algorithms, `--word-diff`, `blame --ignore-revs`) | Internals | ⬜ | |
| 3 | `git notes` | Internals | ⬜ | |
| 4 | Interactive rebase (squash/fixup/autosquash/edit/reorder) | History | ⬜ | |
| 5 | `rebase --onto` | History | ⬜ | |
| 6 | Splitting a commit (`reset -p` / rebase `edit`) | History | ⬜ | |
| 7 | `git bisect` (manual + `bisect run`) | History | ⬜ | |
| 8 | Reflog recovery | History | ⬜ | |
| 9 | `rerere` + `filter-repo` | History | ⬜ | |
| 10 | Cherry-pick backport | Branching | ⬜ | |
| 11 | Merge strategies (`-X ours`/`theirs`, octopus merge) | Branching | ⬜ | |
| 12 | Worktrees | Branching | ⬜ | |
| 13 | Submodule vs subtree | Branching | ⬜ | |
| 14 | Advanced stash (`-p`, to-branch, multiple) | Branching | ⬜ | |
| 15 | Hooks (`pre-commit`, `commit-msg`, `pre-push`) | Config | ⬜ | |
| 16 | `.gitattributes` (diff/merge drivers, union merge, EOL) | Config | ⬜ | |
| 17 | Git LFS | Config | ⬜ | |
| 18 | Signing (GPG/SSH commits & tags + verify) | Config | ⬜ | |
| 19 | Conditional config (`includeIf`) | Config | ⬜ | |
| 20 | Sparse-checkout + shallow/partial clone | Exchange | ⬜ | |
| 21 | `format-patch` / `git am` | Exchange | ⬜ | |
| 22 | `git bundle` / `git archive` + `git maintenance` | Exchange | ⬜ | |
| 23 | Branch protection + CODEOWNERS + required checks + merge queue | GitHub | ⬜ | |
| 24 | GitHub Actions (matrix, reusable/composite workflows, environments) | GitHub | ⬜ | |
| 25 | Release engineering (semver tags, notes, Dependabot, merge strategies) | GitHub | ⬜ | |

Status legend: ⬜ not started · 🟨 in progress · ✅ done

## The toy app

A tiny Python CLI (`gitdojo`) that prints a random quote from a local JSON
file. Deliberately trivial — see `src/gitdojo/`.

```
python -m gitdojo
```
