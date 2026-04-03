# P017 Minimum Straight Line Pickup Routes

## Summary

A company has a base location and several pickup points in the city. It wants to cover all pickup points using the fewest straight-line routes starting from the base.

Each route is an entire straight line through the base location, so multiple pickup points on the same line can share one route.

Given the base coordinates and all pickup points, print the minimum number of routes needed.

## Matching Hints

- The story is about a transportation service in the city of Nazeriana.
- The input starts with `N X0 Y0`, followed by `N` pickup coordinates `Xi Yi`.
- The goal is to minimize the number of straight-line routes from the base.
- All pickup locations must be covered.

## Notes

- Reduce each vector `(Xi - X0, Yi - Y0)` by `gcd(|dx|, |dy|)` to get its direction.
- Because a route is a full line, `(dx, dy)` and `(-dx, -dy)` represent the same route.
- The answer is the number of distinct normalized directions.
