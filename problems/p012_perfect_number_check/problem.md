# P012 Perfect Number Check

## Summary

A perfect number is a number equal to the sum of all its proper factors.

Given an integer `N`, determine whether `N` is a perfect number.

Print `1` if it is perfect, otherwise print `0`.

## Matching Hints

- The statement defines a perfect number as equal to the sum of all its factors.
- The task asks to check whether a given number `N` is a perfect number.
- Output is `1` for a perfect number and `0` otherwise.
- The constraint shown in the screenshot is `0 <= N <= 10^5`.

## Notes

- Proper factors exclude the number itself.
- `0` and `1` are not perfect numbers.
- Sum divisors in pairs up to `sqrt(N)` for efficient `O(sqrt(N))` time.
- Input format in the screenshot is:
  `N`
