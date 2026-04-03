from math import gcd


def solve():
    n, x0, y0 = map(int, input().split())

    lines = set()

    for _ in range(n):
        x, y = map(int, input().split())
        dx = x - x0
        dy = y - y0

        g = gcd(abs(dx), abs(dy))
        dx //= g
        dy //= g

        # A route is a full line through the base, so opposite directions are the same.
        if dx < 0 or (dx == 0 and dy < 0):
            dx = -dx
            dy = -dy

        lines.add((dx, dy))

    print(len(lines))


if __name__ == "__main__":
    solve()
