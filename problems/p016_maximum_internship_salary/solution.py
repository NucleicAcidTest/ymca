import sys


def solve():
    input = sys.stdin.readline

    n = int(input())

    dp0 = 0
    dp1 = 0
    dp2 = 0

    for _ in range(n):
        easy, hard = map(int, input().split())

        new_dp0 = max(dp0, dp1, dp2)
        new_dp1 = max(dp0, dp1, dp2) + easy
        new_dp2 = dp0 + hard

        dp0, dp1, dp2 = new_dp0, new_dp1, new_dp2

    print(max(dp0, dp1, dp2))


if __name__ == "__main__":
    solve()
