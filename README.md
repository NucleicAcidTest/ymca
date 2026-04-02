# Problem Archive

This repository stores coding problems, their Python solutions, and a small local index for quick lookup.

## Layout

- `problems/index.json`: machine-friendly problem index
- `problems/pXXX_slug/problem.md`: normalized problem summary and matching hints
- `problems/pXXX_slug/solution.py`: archived solution for that problem
- `solution.py`: compatibility entry for the most recently solved problem

## Workflow

When a new problem is solved:

1. Create a new `problems/pXXX_slug/` folder.
2. Save the final Python answer in `solution.py`.
3. Record the problem summary, tags, and sample fingerprint in `problem.md`.
4. Update `problems/index.json`.

This makes repeated questions easy to detect from their statement, sample input/output, or core keywords.
