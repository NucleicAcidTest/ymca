---
name: problem-lookup-workflow
description: Use this skill when working in the shl problem archive and the main goal is to quickly check whether a screenshot or problem statement already exists in the local archive. Query first with lookup.py, return the match result in a compact format, and only continue to overwrite, archive, or solve when the user explicitly asks or the request already says to do so.
---

# Problem Lookup Workflow

Use this skill for fast problem-query work in this repository.

The priority is:

1. Query fast
2. Return the local match result clearly
3. Only then decide whether to update, archive, or solve

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

4. Stop after the query result unless the user explicitly wants more, or the request already says things like:
- "if it exists, overwrite it; otherwise archive it"
- "if there is a match, update the answer"
- "if there is no match, solve it directly"

5. When further action is required:
- If lookup returns a match, verify the statement, examples, and provided answer actually fit the matched archived problem before editing any files.
- If lookup returns no match and the user only asked to check, report that clearly and stop.
- If lookup returns no match and the user also wants solving or archiving, continue with the repository's archive workflow.

## Follow-Up Actions

Only do this section when the request clearly asks for it.

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
- match the visible assessment template when one exists
- use `input()`-style line reading by default for these screenshot-based tasks unless the visible template clearly expects EOF-style reading
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

## Query Writing Tips

- Include the core task sentence.
- Include the input format sentence.
- Include at least one sample input/output pair when visible.
- Keep the query in English if the screenshot is in English.
- Do not dump unrelated OCR noise such as editor boilerplate.
- When a screenshot has a stock assessment layout, ignore boilerplate such as language warnings and focus on story, I/O, constraints, and visible tests.

## Solving Rules For Screenshot Problems

If lookup fails and the workflow continues into solving:

- Prefer the visible platform template over personal style.
- For Python assessment screenshots, default to simple `input()` parsing unless the visible code or problem format clearly needs something else.
- Keep existing function names and `main` structure when visible.
- Respect the shown language version.
- Prefer readable and submission-safe code over cleverness.
- Verify against the visible predefined tests before archiving.

## Response Style

- Be fast and concise.
- Lead with the lookup result, not the reasoning.
- When there is a match, give `problem_id`, title, path, score, and one short sentence on why it matched.
- When there is no match, say that directly and do not start archiving unless requested.
- If the user supplied both the problem and an answer screenshot and asked for the full workflow, query first, then continue.
- If solving is required after a miss, briefly restate the inferred task before giving code or archiving.

## Validation Checklist

- The query result was returned before any optional editing work.
- The matched `problem_id` really describes the same problem.
- The archived solution produces the expected sample output.
- `tests/test_lookup.py` still passes.
- New wording variants that failed before are now discoverable.

## Repo-Specific Notes

- This repo's lookup is metadata-driven, not a full-text search over all source files.
- The most important recall levers are `match_hints`, `sample_input_prefix`, `sample_output`, and `notes` in `problems/index.json`.
- Repeated identical queries may return from `.cache/problem_lookup_cache.json`.
