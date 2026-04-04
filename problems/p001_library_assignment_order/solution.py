def safe_order(available, first, second, first_is_issued):
    first_ok = all(a <= b for row1, row2 in zip(first, second) for a, b in zip(row1, row2))
    second_ok = all(a <= b for row1, row2 in zip(second, first) for a, b in zip(row1, row2))
    issued, required = ((first, second) if first_ok else (second, first)) if first_ok != second_ok else ((first, second) if first_is_issued else (second, first))
    need = []
    for have, total in zip(issued, required):
        row = []
        for got, want in zip(have, total):
            if want < got:
                return [-1]
            row.append(want - got)
        need.append(row)

    done = [False] * len(issued)
    order = []
    for _ in range(len(issued)):
        pick = next((i for i in range(len(issued)) if not done[i] and all(a <= b for a, b in zip(need[i], available))), -1)
        if pick < 0:
            return [-1]
        done[pick] = True
        order.append(pick)
        available = [a + b for a, b in zip(available, issued[pick])]
    return order


def main():
    try:
        header = []
        while not header:
            header = input().split()
    except EOFError:
        return
    header = list(map(int, header))
    read = lambda: list(map(int, input().split()))

    if len(header) == 1:
        subjects = header[0]
        available = read()
        students, cols1 = read()
        first = [read() for _ in range(students)]
        students2, cols2 = read()
        second = [read() for _ in range(students)]
        if len(available) != subjects or students2 != students or any(len(row) != cols1 for row in first) or any(len(row) != cols2 for row in second):
            raise ValueError("unsupported input format")
        print(*safe_order(available, first, second, True))
        return

    if len(header) == 2:
        students, subjects = header
        available = read()
        first = [read() for _ in range(students)]
        second = [read() for _ in range(students)]
        if len(available) != subjects or any(len(row) != subjects for row in first + second):
            raise ValueError("unsupported input format")
        print(*safe_order(available, first, second, False))
        return

    raise ValueError("unsupported input format")


if __name__ == "__main__":
    main()
