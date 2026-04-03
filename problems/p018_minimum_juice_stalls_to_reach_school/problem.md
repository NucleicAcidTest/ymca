# P018 Minimum Juice Stalls To Reach School

## Summary

John must walk from home to school over total distance `D`, starting with energy `K`.

Walking one unit of distance consumes one unit of energy, and each juice stall on the way can restore energy equal to the liters available there.

Print the minimum number of stalls John must stop at to reach school, or `-1` if reaching school is impossible.

## Matching Hints

- John misses his bus and has to walk from home to school.
- The input gives `N`, then stall distances `dist_i`, then juice liters `lit_i`, then `D` and `K`.
- The answer is the minimum number of juice stalls John should stop at.
- If John cannot reach the school, print `-1`.

## Notes

- Treat the school as the final checkpoint with zero extra juice.
- Keep all reachable stall juice amounts in a max-heap.
- When current energy is insufficient to reach the next checkpoint, consume juice from the best previously reachable stall.
