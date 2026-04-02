# P007 Smallest Registration Permutation

## Summary

Given an integer registration number:

- digits are from `0` to `9`
- the number may be positive or negative

Generate the smallest permutation of its digits such that the resulting number does not start with zero.

## Matching Hints

- The statement talks about a car racing game and registration numbers.
- A negative registration number means the car is already registered.
- The track number is the smallest permutation of the registration number and never starts with zero.

## Notes

- For positive numbers, sort digits ascending and move the first non-zero digit to the front.
- For negative numbers, to get the smallest numeric value, maximize the absolute value by sorting digits descending and then apply the negative sign.
