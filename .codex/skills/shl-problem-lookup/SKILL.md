---
name: shl-problem-lookup
description: Use this skill when working in the shl problem archive and the main goal is to quickly check whether a screenshot or problem statement already exists in the local archive. Query first with lookup.py, return the match result in a compact format, and if there is no local match then continue by solving the problem and returning the solution unless the user explicitly asked for lookup only. Ask about archiving only after returning the solve result.
---

# SHL Problem Lookup

Use this skill for fast problem-query work in this repository.

The priority is:

1. Query fast
2. Return the local match result clearly
3. If there is no local match, solve and return
4. Only then decide whether to archive or update repository files

## When To Use

Trigger this skill when the user asks any variation of:

- "check whether this problem already exists"
- "see if we solved this before"
- "test the local lookup"
- "just query this problem"
- "find the matching archived problem quickly"
- "if it exists, overwrite it; otherwise archive it"
- "update the archived answer with my solution"

## Screenshot Reading Pattern

Most problems in this repo come from similar coding-assessment screenshots. Read them in this order:

1. Left panel:
- problem story
- `Input`
- `Output`
- `Constraints`
- `Example`

2. Right panel:
- language and version such as Python 3.12
- visible template code
- whether `main` already exists
- whether the platform says `Write your code here`

For this repository, treat the visible assessment language as contextual evidence, not the default output language. The default solution language for `shl` archive work is Python 3.12 unless the user explicitly asks for another language or explicitly asks for a direct submission snippet matching the screenshot language.

For Python screenshot problems in this repository, treat the visible template shape as a hard constraint, not a style preference:

- default to `input()`-based line reading
- include a `main()` function in archived Python solutions
- keep an existing visible `main()` shape when the screenshot shows one
- only switch to bulk `sys.stdin.buffer.read()` parsing when the screenshot or problem format clearly requires it

3. Bottom test area:
- predefined test inputs
- expected outputs
- any mismatch between examples and visible tests

If the screenshot is blurry or cropped, say exactly what is unreadable. Do not invent hidden signatures or hidden test cases.

## Files That Matter

- `lookup.py`: CLI entrypoint
- `problems/lookup.py`: lookup logic and scoring
- `problems/index.json`: searchable metadata for every archived problem
- `problems/pXXX_slug/problem.md`: human summary of the archived problem
- `problems/pXXX_slug/solution.py`: archived answer
- `tests/test_lookup.py`: lookup regression tests

## Query-First Workflow

1. Read the problem statement from user text or screenshots and compress it into one query paragraph.
2. Run:

```powershell
python lookup.py --json --query "<problem summary here>"
```

3. Return the result immediately in this format:

If found:

```text
Found local match
problem_id: pXXX
title: ...
path: problems/pXXX_slug/solution.py
score: ...
match_type: ...
```

If not found:

```text
No local match
query summary: ...
next step: wait / solve / archive
```

4. Stop after the query result only when the user explicitly asked for lookup only.

5. If lookup misses and the user did not explicitly limit the task to lookup-only, continue automatically into solving.

6. When further action is required:
- If lookup returns a match, verify the statement, examples, and provided answer actually fit the matched archived problem before editing any files.
- If lookup returns no match and the user only asked to check, report that clearly and stop.
- If lookup returns no match, the default action is to solve the problem and return the solution first.
- After returning a fresh solution for a miss, ask whether to archive it into the repository.
- If lookup returns no match and the user already asked for solving or archiving, continue with the repository's archive workflow immediately.

Treat these requests as permission to continue beyond lookup:
- "if it exists, overwrite it; otherwise archive it"
- "if there is a match, update the answer"
- "if there is no match, solve it directly"

## Follow-Up Actions

Only do this section when the request clearly asks for it, or after a lookup miss has already been solved and the next decision is whether to archive.

### If Found And User Wants Update

- Update the archived `solution.py`.
- If the wording variant was not well covered, strengthen `match_hints`, sample fingerprints, or notes in `problems/index.json` and `problem.md`.

### If Not Found And User Wants Archive

- add a new folder under `problems/`
- add `problem.md`
- add `solution.py`
- update `problems/index.json`
- point `solution.py` at the latest solved problem if that is the current repo convention
- add or update a `tests/test_lookup.py` case for the new wording

### If Not Found And User Wants A Fresh Solution

- solve the problem normally
- default to Python 3.12 for this repository
- only switch to the screenshot language when the user explicitly asks for that language or asks for a direct submission snippet that must match the visible platform language
- match the visible assessment template when one exists, but do not let the visible language override the repository default on its own
- use `input()`-style line reading by default for these screenshot-based tasks unless the visible template clearly expects EOF-style reading
- archived Python solutions should include `main()` by default, even when the screenshot only shows a blank `Write your code here` area
- keep `main` unchanged when the screenshot already provides one
- write code only under `Write your code here` when the user asks for direct submission format
- do not add debug prints, prompts, or extra comments
- if the repo workflow requires archiving solved problems, archive it after solving

### Archiving Rules For Newly Solved Screenshot Problems

When archiving a newly solved screenshot problem:

- create the new `pXXX` folder and index entry
- capture the screenshot wording variant in `match_hints`
- record visible sample inputs and outputs when readable
- store the final verified solution, not a draft stub
- add a lookup regression test using the screenshot's wording

## Validation After Changes

Only run this section when files were changed:

```powershell
python lookup.py --json --query "<same summary>"
python -m unittest discover -s tests -v
```

Also run sample input through the archived solution when sample I/O is available.

## Matching Rules

- Prefer exact local lookup over manual guesswork.
- Use the screenshots' story wording, input format, and sample output in the query. These are often the strongest signals.
- Do not assume two problems are the same just because the implementation pattern looks similar.
- If the user-provided answer screenshot obviously belongs to a different problem, stop and ask for the correct answer instead of overwriting anything.
- If the user only asked to query, do not edit files.
- If the user did not ask for lookup-only and there is no match, do not stop at "No local match"; solve the problem next.

## Query Writing Tips

- Include the core task sentence.
- Include the input format sentence.
- Include at least one sample input/output pair when visible.
- Keep the query in English if the screenshot is in English.
- Do not dump unrelated OCR noise such as editor boilerplate.
- When a screenshot has a stock assessment layout, ignore boilerplate such as language warnings and focus on story, I/O, constraints, and visible tests.

## Solving Rules For Screenshot Problems

If lookup fails and the workflow continues into solving:

- For this repo, prefer Python 3.12 unless the user explicitly requests another language.
- Prefer the visible platform template over personal style only after the output language is settled.
- Do not infer Java, C++, or another language purely from the screenshot selector when the task is repo-centric lookup/solve work.
- For Python assessment screenshots, default to simple `input()` parsing unless the visible code or problem format clearly needs something else.
- For archived Python answers, include a `main()` function by default and call it from the usual `if __name__ == "__main__":` guard.
- Keep existing function names and `main` structure when visible.
- Respect the shown language version.
- Prefer readable and submission-safe code over cleverness.
- Verify against the visible predefined tests before archiving.

## Python Output Contract

When this skill produces or overwrites an archived Python solution for a screenshot-based SHL problem, the default contract is:

- use `input()` / `input().split()` style parsing unless the statement clearly forces another format
- define `main()`
- keep `if __name__ == "__main__": main()`
- avoid replacing a visible `main()`-based template with buffer-wide parsing just for convenience
- if a helper such as `solve()` is added, it should delegate to `main()` rather than replace it

If you are about to return or archive a Python solution that does not satisfy this contract, stop and fix the code first.

## Response Style

- Be fast and concise.
- Lead with the lookup result, not the reasoning.
- When there is a match, give `problem_id`, title, path, score, and one short sentence on why it matched.
- When there is no match, say that directly and do not start archiving unless requested.
- If the user supplied both the problem and an answer screenshot and asked for the full workflow, query first, then continue.
- If there is no local match, return both the miss result and the fresh solution in the same turn unless the user asked for lookup-only.
- If solving is required after a miss, briefly restate the inferred task before giving code, then ask whether to archive it.

## Validation Checklist

- The query result was returned before any optional editing work.
- A lookup miss did not end the workflow when the user expected the problem to be solved.
- The matched `problem_id` really describes the same problem.
- The archived solution produces the expected sample output.
- `tests/test_lookup.py` still passes.
- New wording variants that failed before are now discoverable.
- Any archived Python solution for a screenshot-based problem uses `input()` by default unless there was a concrete reason not to.
- Any archived Python solution for a screenshot-based problem has a `main()` function and standard `__main__` guard.

## Repo-Specific Notes

- This repo's lookup is metadata-driven, not a full-text search over all source files.
- The most important recall levers are `match_hints`, `sample_input_prefix`, `sample_output`, and `notes` in `problems/index.json`.
- Repeated identical queries may return from `.cache/problem_lookup_cache.json`.
