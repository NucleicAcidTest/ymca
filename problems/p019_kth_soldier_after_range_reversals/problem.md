# P019 Kth Soldier After Range Reversals

## Summary

There are `N` soldiers standing in positions `1..N`, and initially soldier ID `i` stands at position `i`.

Each action round chooses positions `L` and `R` and reverses the whole segment `[L, R]`.

After `Q` rounds, print the ID of the soldier standing at position `K`.

## Matching Hints

- The story says there are `N` soldiers standing in a line with IDs from `1` to `N`.
- Each round gives `Li` and `Ri`, and the soldiers swap in pairs until the interval is reversed.
- The input starts with `N Q K`, followed by `Q` lines of `Li Ri`.
- The task asks for the ID of the soldier at the `K`th position after all rounds.

## Notes

- Reversing `[L, R]` maps any position `x` inside the interval to `L + R - x`.
- Work backward from the final position `K` through the operations in reverse order.
- Because the initial ID equals the initial position, the recovered position is the answer.
