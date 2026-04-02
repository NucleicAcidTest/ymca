import sys


def block_leq(a, b):
    return all(x <= y for row_a, row_b in zip(a, b) for x, y in zip(row_a, row_b))


def parse_input(tokens):
    idx = 0

    m = tokens[idx]
    idx += 1

    avail = tokens[idx:idx + m]
    idx += m

    n = tokens[idx]
    req_books = tokens[idx + 1]
    idx += 2

    block1 = []
    for _ in range(n):
        block1.append(tokens[idx:idx + req_books])
        idx += req_books

    _students_with_books = tokens[idx]
    issued_books = tokens[idx + 1]
    idx += 2

    block2 = []
    for _ in range(n):
        block2.append(tokens[idx:idx + issued_books])
        idx += issued_books

    # The screenshot text and example disagree on block order.
    # Prefer the arrangement where issued[i][j] <= required[i][j].
    if block_leq(block1, block2) and not block_leq(block2, block1):
        issued, required = block1, block2
    elif block_leq(block2, block1) and not block_leq(block1, block2):
        issued, required = block2, block1
    else:
        # Fall back to the order shown by the example.
        issued, required = block1, block2

    return avail, issued, required


def safe_order(avail, issued, required):
    n = len(issued)
    m = len(avail)

    need = []
    for i in range(n):
        row = []
        for j in range(m):
            if required[i][j] < issued[i][j]:
                return [-1]
            row.append(required[i][j] - issued[i][j])
        need.append(row)

    done = [False] * n
    order = []
    current = avail[:]

    for _ in range(n):
        chosen = -1
        for i in range(n):
            if done[i]:
                continue
            if all(need[i][j] <= current[j] for j in range(m)):
                chosen = i
                break

        if chosen == -1:
            return [-1]

        done[chosen] = True
        order.append(chosen)
        for j in range(m):
            current[j] += issued[chosen][j]

    return order


def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    tokens = list(map(int, data))
    avail, issued, required = parse_input(tokens)
    ans = safe_order(avail, issued, required)
    print(*ans)


if __name__ == "__main__":
    main()
