def solve():
    n, q, k = map(int, input().split())
    ops = [tuple(map(int, input().split())) for _ in range(q)]

    for left, right in reversed(ops):
        if left <= k <= right:
            k = left + right - k

    print(k)


if __name__ == "__main__":
    solve()
