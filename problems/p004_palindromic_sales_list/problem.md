# P004 Palindromic Sales List

## Summary

Given a list of positive integers, repeatedly merge any two consecutive elements into their sum so that the final list becomes a palindrome.

Among all possible palindromic results, output one with maximum length.

## Notes

- Maximum final length means using the fewest merges.
- A greedy two-pointer strategy works:
  compare both ends, and keep merging the side with the smaller running sum until both sides match.
