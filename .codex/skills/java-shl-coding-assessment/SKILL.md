---
name: java-shl-coding-assessment
description: Produce compact, runnable Java 21 solutions and JUnit 5 tests for SHL online coding assessments or interview programming tasks. Use when the user asks for Java SHL answers, compressed Java code for word/character limits, LeetCode-style `Solution.solve(...)` methods, `Scanner` stdin/stdout handling, strict Java import/exception/style constraints, or per-case `SolutionTest` coverage with extra boundary tests.
---

# Java SHL Coding Assessment

## Overview

Turn SHL or interview coding prompts into concise Java 21 submissions with a pure `Solution.solve(...)` core, a `Scanner`-based `main`, and focused JUnit 5 tests when requested.

## Priority Order

Follow these priorities when requirements conflict:

1. Visible platform template, required class name, method signature, and return type.
2. Problem statement input-output format and examples.
3. User's latest instruction for direct submission code, full files, or tests.
4. Correctness, asymptotic complexity, and edge-case coverage.
5. Compactness and style constraints.

Do not rename or reshape a visible required method just to satisfy a style rule.

## Workflow

1. Read the whole problem.
- Extract input, output, constraints, examples, and hidden assumptions from screenshots or text.
- If a screenshot shows Java template code, preserve the visible `Solution`, `solve`, and `main` shape.
- State unreadable or ambiguous parts only when they affect correctness or code placement.

2. Design the core method first.
- Use `class Solution`.
- Put the algorithm in `public static ... solve(...)`.
- Match method parameters to the logical problem input.
- Match the return type to the final answer.
- Keep `solve` pure: no stdin reads, stdout writes, prompts, or debug output.

3. Add console I/O only when a full submission program is needed.
- Implement `public static void main(String[] args)`.
- Use `Scanner` for standard input and output.
- Do not declare `throws` on `main`.
- Catch only specific exceptions when unavoidable, such as `IOException`; do not catch or throw generic `Exception`.
- For fixed-size input, read exactly enough values, call `solve`, print the result, and return.
- For variable or unbounded groups, read line by line and output each completed case immediately instead of waiting for all input.

4. Verify before answering.
- Check every visible example and provided test case.
- Add mental checks for minimum input, maximum input shape, duplicates, zero, negative values when allowed, empty-looking cases, single-element cases, and all-equal cases.
- Prefer optimal time and space complexity that remains simple enough for SHL submission.

## Java Style Rules

- Use Java 21-compatible standard library code only.
- Use exact imports, never wildcard imports.
- Use semantic lowerCamelCase names for variables and methods.
- Keep user-chosen names at least 4 characters long, except platform-required names such as `args`.
- Use `Solution` exactly for the class name.
- Do not declare and initialize multiple variables in one statement, such as `int left = 0, right = 1;`.
- Do not add dead code, redundant comments, prompts, or debug prints.
- Keep code compact, but never make it clever at the cost of correctness.
- Remember primitive/generic boxing: use `Integer`, `Long`, etc. in generic collections.
- Arrays may be collection elements, such as `List<int[]>`.
- Collections must not be array elements, such as `List<Integer>[]`.

## Import Rules

Add only imports that are actually used. Common allowed examples:

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
```

Never use:

```java
import java.util.*;
```

## Testing Rules

When the user asks for tests or local artifacts:

- Create `SolutionTest` with JUnit 5.
- Write one independent test method for each example and each provided test case.
- Add 10 additional tests covering boundary and easy-to-miss cases.
- Test `Solution.solve(...)` directly rather than stdin/stdout unless console parsing itself is the point.
- Run the available Java test command when the project has Maven, Gradle, or another obvious test runner.
- If no runner exists, provide self-contained test files and state that local execution was not available.

## Output Style

- If the user asks for direct SHL submission code, return only the Java code block.
- If the user asks for explanation plus code, keep the explanation short and operational, then provide code.
- If the user asks for full files, provide `Solution.java` and `SolutionTest.java`.
- Mention assumptions around ambiguous input grouping, hidden templates, or unreadable screenshot text.
