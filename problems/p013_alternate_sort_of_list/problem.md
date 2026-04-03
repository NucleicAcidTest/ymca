# P013 Alternate Sort Of List

## Summary

Sort the given list in ascending order, then take every alternate element starting from the first position.

Print the selected elements as space-separated integers.

## Matching Hints

- The statement says "alternate sort of a list".
- Alternate elements are taken starting from the first position after sorting in ascending order.
- Input contains the list size followed by `N` unsorted integers.
- Output is the alternately sorted elements printed with spaces.

## Notes

- After sorting, the required output is exactly the elements at indices `0, 2, 4, ...`.
- The example shown is `3 5 1 5 9 10 2 6`, which sorts to `1 2 3 5 5 6 9 10` and outputs `1 3 5 9`.
- The two screenshots are the same problem in different language tabs.
- Input format in the screenshots is:
  `N`
  `arr[0] arr[1] ... arr[N-1]`
