# P006 Minimum Cable Length

## Summary

Systems are placed on a line. Some are initially ON (`1`), others are OFF (`0`).

An OFF system can be connected to the nearest already-ON system so that it becomes ON as well, and then it can help connect other OFF systems.

Find the minimum total cable length needed to make all systems ON.

## Matching Hints

- The statement mentions systems in a row with ON (`1`) or OFF (`0`) state.
- Distances of systems from the first system are given.
- The sample input is:
  `3`
  `1 0 0`
  `1 5 6`
  with output `5`.

## Notes

- For OFF systems before the first ON, connect them as one chain to that ON.
- For OFF systems after the last ON, connect them as one chain to that ON.
- Between two ON systems, connect everything except the largest adjacent gap in that segment.
