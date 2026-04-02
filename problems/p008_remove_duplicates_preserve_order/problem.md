# P008 Remove Duplicates Preserve Order

## Summary

Given a list of integers, remove duplicate values so that only the first occurrence of each number remains, while preserving the original order.

## Matching Hints

- The statement says to remove all duplicate numbers.
- The output should contain only distinct numbers.
- The order of the remaining numbers must stay the same as in the input.

## Notes

- Track seen values with a set.
- Append a number to the result only the first time it appears.
