# P003 Dictionary Subsequence Filter

## Summary

Given:

- a master word `s`
- an integer `N`
- `N` dictionary words

Find all dictionary words that can be formed by deleting some characters from the master word while preserving the original order of the remaining characters.

In other words, output all dictionary words that are subsequences of the master word, preserving the order in which the words appear in the dictionary.

## Matching Hints

- The statement says `Given a dictionary of N words and a master word`.
- It asks for words formed by deleting some characters of the master word.
- The valid words must be printed in dictionary order.

## Notes

- Build a list of positions for each character in the master word.
- For each dictionary word, greedily match the next valid position with binary search.
- If no dictionary word matches, print `-1`.
