# P022 Shortest Route With Magic Spell

## Summary

Given `n` cities and `m` bidirectional weighted roads, find the shortest route from city `A` to city `B`.

A magician may cast a magic spell at most `K` times, and each cast can make one chosen road on the route contribute `0` distance instead of its original weight.

Print the minimum possible route length after using up to `K` spells, or `-1` if city `B` is unreachable from city `A`.

## Matching Hints

- The first line consists of five space-separated integers `n m A B K`.
- The next `m` lines each contain `u v w` for a bidirectional road between two cities.
- Print the length of the shortest route between the two given cities after performing the magic spell `K` number of times.
- If no path exists between the two cities, print `-1`.
- A visible example uses `5 5 0 3 1` and returns `1` after making edge `4 3` free.

## Notes

- Use Dijkstra on state `(city, spells_used)`.
- From state `(u, used)`, each road `(u, v, w)` gives two transitions: pay `w`, or pay `0` if `used < K`.
- The first time the destination is popped from the min-heap is the optimal answer.
- A visible predefined case with `4 2 0 2 1 / 0 1 5 / 2 3 6` returns `-1`.
