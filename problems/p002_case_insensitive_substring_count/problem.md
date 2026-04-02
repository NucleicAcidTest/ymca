# P002 Case-Insensitive Substring Count

## Summary

Given two strings containing only English letters:

- `parent`: the main string
- `sub`: the string to search for

Count how many times `sub` occurs in `parent`, ignoring letter case. If there is no occurrence, print `0`.

The archived solution counts overlapping matches as valid occurrences.

## Matching Hints

- The statement mentions `countOccur(parent, sub)`.
- It says to disregard the case of the letters.
- The sample input uses a string containing `Tim` three times and outputs `3`.

## Notes

- Convert both strings to lowercase first.
- Scan all possible start positions and compare slices.
