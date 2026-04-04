def main() -> None:
    size = int(input().strip())
    numbers = list(map(int, input().strip().split()))

    numbers.sort()
    result = numbers[:size:2]
    print(" ".join(map(str, result)))


def solve():
    main()


if __name__ == "__main__":
    main()
