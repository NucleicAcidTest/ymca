# P009 LRU Cache Misses

## Summary

Given a cache of fixed size and a sequence of page requests, count the number of cache misses under the Least Recently Used (LRU) policy.

- If a requested page is already in cache, it becomes the most recently used page.
- If it is not in cache, that is a cache miss.
- If the cache is full, remove the least recently used page first.

## Matching Hints

- The statement mentions virtual memory management.
- It explicitly says Least Recently Used (LRU) cache.
- Input includes page requests and cache size.
- Output is the number of cache misses.

## Notes

- Keep cache pages in recency order.
- On a hit, move the page to the most recent position.
- On a miss, increment the answer and evict the least recent page if needed.
