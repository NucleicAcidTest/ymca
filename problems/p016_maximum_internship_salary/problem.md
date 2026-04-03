# P016 Maximum Internship Salary

## Summary

Stephen works for `N` internship days. On each day, he may take an easy task, a difficult task, or skip work.

He may take a difficult task only on the first day or on a day whose previous day was skipped.

Given the daily pay for easy and difficult tasks, compute the maximum salary he can earn.

## Matching Hints

- The statement is about Stephen doing an internship for `N` days.
- Each day offers an easy task and a difficult task, and skipping is also allowed.
- A difficult task can only be chosen on day one or after a day with no work.
- The goal is to calculate the maximum salary.

## Notes

- Use dynamic programming with three states: skip, easy, and hard.
- The new hard state can only come from the previous skip state.
- The screenshot examples include `4 / 1 2 / 4 10 / 20 21 / 2 23` with output `33`, and `4 / 7 10 / 6 7 / 4 6 / 6 7` with output `26`.
