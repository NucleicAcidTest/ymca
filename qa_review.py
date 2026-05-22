from math import gcd


def normalize_line(dx, dy):
    common = gcd(abs(dx), abs(dy))
    dx //= common
    dy //= common

    if dx < 0 or (dx == 0 and dy < 0):
        dx = -dx
        dy = -dy

    return dx, dy


def main():
    n, base_x, base_y = map(int, input().split())
    routes = set()

    for _ in range(n):
        x, y = map(int, input().split())
        dx = x - base_x
        dy = y - base_y

        if dx == 0 and dy == 0:
            continue

        routes.add(normalize_line(dx, dy))

    print(len(routes))


if __name__ == "__main__":
    main()