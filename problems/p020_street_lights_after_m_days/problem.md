# P020 Street Lights After M Days

## Summary

There are `N` street lights in a row, each with state `0` or `1`.

For the next day, a light becomes `0` when its left and right adjacent lights are both `0` or both `1`; otherwise it becomes `1`.

For the two end lights, the missing outside neighbor is assumed to be `0`.

Given `N`, the current state as `N` space-separated integers, and the number of days `M`, print the state of the street lights after `M` days.

## Matching Hints

- Mr. Woods, an electrician, has made some faulty connections of eight street lights in Timberland city.
- If the adjacent street lights to a particular light are both ON or both OFF, then that street light goes OFF the next night.
- Otherwise, the street light remains ON on the next night.
- The two street lights at the ends of the road have only one single adjacent street light, and the other adjacent light can be assumed to be always OFF.
- The input section says the first line is the number of street lights, the second line is `N` space-separated `0/1` values, and the last line is `days`.

## Notes

- The next value of each light is exactly the XOR of its two neighbors.
- The archived statement follows the left-panel problem text: spaced input values and spaced output values.
- The solution still accepts a compact binary-string variant as a fallback because the bottom test widget in the screenshot is visually ambiguous.
- The example `8 / 1 1 1 0 1 1 1 1 / 2` returns `0 0 0 0 0 1 1 0`.
