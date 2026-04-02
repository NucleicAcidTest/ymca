# P001 Library Assignment Order

## Summary

There are `M` types of books in a library and `N` students.

- `avail[j]` is the current number of available books for subject `j`.
- `issued[i][j]` is the number of books of subject `j` already issued to student `i`.
- `required[i][j]` is the total number of books of subject `j` student `i` needs to complete the assignment.

A student `i` can complete the assignment if:

`required[i][j] - issued[i][j] <= avail[j]` for every subject `j`.

Once student `i` completes the assignment, they return all `issued[i][j]` books to the library, so the available stock increases by that row.

Output the optimal sequence of student IDs so all students can complete their assignments. If multiple students are available at the same time, choose the smaller student ID first. If no full sequence exists, output `-1`.

## Matching Hints

- The problem statement mentions `booksNum`, `avail`, `studentNum`, `reqBooks`, and `studentIssuedBooks`.
- The sample output is `2 0 1`.
- The core pattern is the same as Banker's Algorithm / safe sequence.

## Parsing Note

The screenshot for this problem has a mismatch between the text description and the example ordering of the `issued` and `required` blocks. The archived solution auto-detects the sensible order and falls back to the example ordering.
