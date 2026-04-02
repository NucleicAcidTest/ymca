# P005 Top-Left Submatrix Product Count

## Summary

Given an `N x M` matrix of non-negative integers, count how many non-empty submatrices:

- contain the top-left element `A[0][0]`
- have product of all elements less than or equal to `K`

Because the submatrix must contain the top-left element, every valid submatrix is exactly a prefix rectangle `A[0..x][0..y]`.

## Matching Hints

- The statement asks for submatrices that contain the top left element.
- It asks for product less than or equal to `K`.
- The sample input includes:
  `2 3`
  `1 2 3`
  `1 2 3`
  `3`

## Notes

- Any prefix rectangle containing a zero has product `0`, so it is valid when `K >= 0`.
- For non-zero prefixes, cap products at `K + 1` to avoid overflow and unnecessary large multiplication.
