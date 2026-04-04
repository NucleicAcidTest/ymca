def main():
    n = int(input().strip())
    counts = list(map(int, input().split()))
    counts = counts[:n]

    total = sum(counts)
    mx = max(counts)

    print(min(total, 2 * (total - mx) + 1))


def solve():
    main()


if __name__ == "__main__":
    main()
