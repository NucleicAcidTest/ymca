# P021 Maximum Trading Days Without Same Town

## Summary

Moche Goldberg trades in `N` towns numbered `1..N`.

Each day he chooses one town to sell his products. The chosen towns on any two successive days must be different, and town `i` can be chosen at most `c_i` times.

Print the maximum number of days he can operate.

## Matching Hints

- Moche Goldberg starts trading in `N` towns numbered `1` to `N`.
- Every day he sells his products in one of the towns.
- The towns chosen on any two successive days should be different.
- A town `i` can be chosen at most `c_i` times.
- The task asks for the maximum number of days during which the salesman can work.

## Notes

- Let `S = sum(c_i)` and `M = max(c_i)`.
- If the most frequent town can be separated by all other visits, the answer is `S`.
- Otherwise the best possible arrangement length is `2 * (S - M) + 1`.
- A visible predefined case with `4` and `2 2 2 2` returns `8`.
- Another visible case with `3` and `7 2 3` returns `11`.
