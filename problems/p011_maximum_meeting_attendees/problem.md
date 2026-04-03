# P011 Maximum Meeting Attendees

## Summary

There are `N` CEOs labeled from `0` to `N - 1`.

Each CEO likes exactly one other CEO, given by `personIDs[i]`. A CEO will attend the meeting only if they can sit next to the CEO they like.

Find the maximum number of CEOs who can attend.

## Matching Hints

- The statement talks about CEOs, invitation IDs from `0` to `N - 1`, and a favorite CEO for each person.
- Each person likes exactly one other person.
- A CEO attends only if they can sit next to the CEO they like.
- The task asks for the maximum number of attendees.

## Notes

- Model the preferences as a directed graph where each node has out-degree `1`.
- The answer is the maximum of:
  `1.` the length of the largest directed cycle
  `2.` the sum over every mutual pair `(a, b)` with `a -> b` and `b -> a` of the longest incoming chain ending at `a` plus the longest incoming chain ending at `b`
- Trees feeding into cycles can be peeled with indegree pruning.
- Input format in the screenshot is:
  `N`
  `personIDs[0] personIDs[1] ... personIDs[N-1]`
