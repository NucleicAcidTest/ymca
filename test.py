def solve():
    n, q, k = map(int, input().split())
    ops = [tuple(map(int, input().split())) for _ in range(q)]

    for l, r in reversed(ops):
        if l <= k <= r:
            k = l + r - k

    print(k)


if __name__ == "__main__":
    solve()
