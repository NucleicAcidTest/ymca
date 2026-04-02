def countOccur(parent, sub):
    parent = parent.lower()
    sub = sub.lower()

    if not sub or len(sub) > len(parent):
        return 0

    count = 0
    sub_len = len(sub)

    for i in range(len(parent) - sub_len + 1):
        if parent[i:i + sub_len] == sub:
            count += 1

    return count


def main():
    parent = str(input().strip())
    sub = str(input().strip())

    result = countOccur(parent, sub)
    print(result)


if __name__ == "__main__":
    main()
