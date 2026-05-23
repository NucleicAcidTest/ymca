---
name: shl-coding-assessment
description: Translate image-based SHL or coding-assessment questions and produce submission-ready Python 3.12 answers under exact visible template constraints. Use when the user provides coding-test screenshots, asks for Chinese translation, code to place under `Write your code here`, preservation of `Solution`, `main`, function signatures, console parsing, PEP 8 naming, pytest checks, or quick correctness checks against visible examples and tests.
---

# SHL Coding Assessment Answer

## Overview

Turn coding-assessment screenshots into compact, submission-ready Python 3.12 answers. Extract the prompt, preserve the visible platform template, follow the user's SHL coding style rules, and verify the solution against visible input-output behavior.

## Priority Order

Follow these priorities when rules conflict:

1. Visible platform template and required function signature.
2. Problem statement input-output format.
3. Console behavior that fits the input format and the user's latest instruction.
4. Correctness and full test-case pass rate.
5. PEP 8 naming, layout, compactness, and optional test-delivery rules.

Do not rename or reshape visible template methods just to satisfy style rules.

## Workflow

1. Read every screenshot carefully.
- Inspect the left panel for statement, constraints, examples, and notes.
- Inspect the right panel for language, class, function signature, `main`, and insertion marker.
- Inspect bottom-right test cases. If they conflict with examples and the user asks for priority, prefer bottom-right tests.
- Treat consecutive scroll screenshots as one problem unless clearly different.
- Merge all readable details before solving.

2. State uncertainty early.
- Say exactly which text, signature, or test case is unreadable.
- Use overlapping screenshots to reconstruct missing lines before asking again.
- Ask for a tighter crop only when missing text affects correctness or placement.
- Never invent hidden signatures, hidden parsing code, or invisible tests.

3. Translate when useful.
- Summarize the task in Chinese with input, output, core rule, and visible edge cases.
- Keep the translation short and operational.

4. Produce code under the visible constraints.
- Use Python 3.12 only.
- Use only built-in features and Python 3.12 standard library modules.
- Include all necessary imports in full-program answers.
- Prefer exact module imports such as `import sys`; never use wildcard imports.
- Preserve visible `Solution`, method names, parameters, return type, `main`, and surrounding template.
- If `Write your code here` is visible and the user asks for a fill-in answer, return only code for that region.
- Do not add prompts, debug output, explanatory prints, or comments.

5. Verify before responding.
- Walk through visible examples and predefined tests.
- Check boundary cases: minimum size, empty-looking input, duplicates, all-same values, one active element, zero, negative values when allowed, and large limits.
- Run a local stdin/stdout check when practical and compatible with the inferred format.
- Call out remaining assumptions around hidden `main`, parsing, or ambiguous spacing.

## Python Submission Profile

When the template is not fully visible and a full program is needed:

- Put core logic inside a `Solution` class.
- Include a standard `def main():` entry point.
- End with `if __name__ == "__main__": main()`.
- `Solution` methods return results; `main` parses input and prints the final required output.
- Final required output may use `print`. Debug or prompt prints are forbidden.

## Console Input Rules

- Prefer `sys.stdin.buffer.readline()` when the number of needed lines or tokens is fixed or can be inferred.
- With `readline()`, read until enough data is collected, then compute, print, and return immediately.
- Do not use `sys.stdin.buffer.readlines()`, `list(sys.stdin...)`, or stdin iteration for ordinary SHL fixed-format snippets; these wait for EOF in manual custom tests.
- Use `sys.stdin.buffer.read()` only when the input scale is large and batch parsing is clearly more appropriate.
- If `read()` is used, remember that local manual console tests need EOF before output appears.
- Do not use `input()` unless the prompt is explicitly interactive or the user asks for it.
- Maintain a line or token buffer based on the problem's input format.
- Once one non-multiple-test case is complete, compute, print the answer, and return.
- If screenshot text and predefined tests imply different but compatible layouts, support both with line-by-line parsing that stops as soon as one complete case is available.
- If the statement clearly defines multiple test cases, process exactly the specified number of cases, print required outputs, and return.
- Ignore blank lines when the format allows whitespace noise.
- Support extra spaces between values.
- If the required amount of input cannot be inferred, use line-by-line reading and explain the assumption briefly outside the code.

## Style Rules

- Code must be compact but not at the expense of correctness.
- No comments inside returned code.
- Keep every code line at or below 120 characters.
- Follow PEP 8 naming for user-chosen names.
- Use `snake_case` for variables, functions, and methods.
- Use `PascalCase` for classes, including `Solution`.
- Use `UPPER_SNAKE_CASE` for module-level constants.
- Names should be semantic and usually longer than 3 characters.
- Loop indexes and tiny local counters may use short names such as `i` or `j` when clearer.
- Exceptions: visible platform names, provided signatures, `Solution`, `main`, `self`, `__name__`, and `__main__`.
- Do not use chained assignment such as `leftIndex = rightIndex = 0`.
- Avoid multi-variable assignment or unpacking in user-written code unless a visible template requires it.
- Function signatures may contain multiple parameters when the platform requires them.
- Avoid experimental syntax or features newer than Python 3.12.
- Avoid type hints unless useful; when using them, do not create generic/container type mismatches.

## Testing Rules

- Always mentally verify visible examples and bottom-right predefined tests before responding.
- When local execution is practical, run a quick check against visible samples.
- If the user asks for tests or a full local artifact, provide `solution.py`, `test_solution.py`, and `pytest.ini`.
- In pytest deliverables, use a `SolutionTest` class and include `python_classes = *Test` in `pytest.ini`.
- Put each visible sample in its own test method.
- Add at least 10 extra tests for boundary and easy-to-miss cases when the user asks for test files.
- Do not include pytest files when the user only needs a direct SHL submission snippet.

## Output Style

- If asked for translation and solution, provide translation first and code second.
- If asked for direct submission code, return only the code block or only the fill-in snippet requested.
- If asked for full code and tests, output `solution.py`, then `test_solution.py`, then `pytest.ini`.
- Keep non-code explanation compact.

## Common Pitfalls

- Do not infer Python template details from a Java screenshot.
- Do not treat scroll screenshots of the same page as separate tasks.
- Do not use EOF-style parsing when enough input can be determined from earlier lines.
- Do not answer SHL custom-test snippets with `readlines()` or stdin iteration when `readline()` can read a complete case.
- Do not replace a visible `main` or method signature.
- Do not let style rules break platform-required names.
- Do not stop after matching the sample; check degenerate and boundary cases first.
