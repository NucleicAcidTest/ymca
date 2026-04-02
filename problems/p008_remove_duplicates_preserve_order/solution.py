def distinctInOrder(values):
    seen = set()
    result = []

    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)

    return result


def main():
    size = int(input().strip())
    values = list(map(int, input().split()))
    values = values[:size]

    result = distinctInOrder(values)
    print(" ".join(map(str, result)))


if __name__ == "__main__":
    main()
