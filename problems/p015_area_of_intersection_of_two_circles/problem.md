# P015 Area Of Intersection Of Two Circles

## Summary

Given the centers and radii of two circles, compute the area of their intersection.

The input contains two lines: `x1 y1 r1` for the first circle and `x2 y2 r2` for the second circle.

Print the overlap area rounded to 6 decimal places.

## Matching Hints

- The statement asks for the area of intersection of two circles.
- Each input line contains the center coordinates and radius of one circle.
- The output is a real number rounded to 6 decimal places.
- One sample has `0 0 2` and `3 0 2` with output `1.813247`.

## Notes

- If the circles are disjoint or just touch externally, the overlap area is `0.0`.
- If one circle is fully inside the other, the overlap area is the area of the smaller circle.
- Otherwise compute the lens area as the sum of two circular segments.
