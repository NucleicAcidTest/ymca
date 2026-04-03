import math
import sys


def is_perfect_number(n):
    if n <= 1:
        return 0

    total = 1
    limit = int(math.sqrt(n))

    for divisor in range(2, limit + 1):
        if n % divisor != 0:
            continue

        total += divisor
        other = n // divisor
        if other != divisor:
            total += other

    return 1 if total == n else 0


def main():
    data = sys.stdin.read().strip()
    if not data:
        return

    n = int(data.split()[0])
    print(is_perfect_number(n))


if __name__ == "__main__":
    main()
