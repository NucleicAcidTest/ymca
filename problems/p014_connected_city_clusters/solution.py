def count_clusters(matrix):
    n = len(matrix)
    visited = [False] * n
    clusters = 0

    for start in range(n):
        if visited[start]:
            continue

        clusters += 1
        stack = [start]
        visited[start] = True

        while stack:
            node = stack.pop()
            row = matrix[node]

            for neighbor, connected in enumerate(row):
                if connected and not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)

    return clusters


def main():
    tokens = []
    try:
        while True:
            parts = input().split()
            if parts:
                tokens.extend(map(int, parts))
    except EOFError:
        pass
    if not tokens:
        return

    if len(tokens) < 2:
        print(0)
        return

    n = tokens[0]
    cols = tokens[1]
    pos = 2
    matrix = []

    for _ in range(n):
        row = tokens[pos:pos + cols]
        pos += cols
        matrix.append(row[:n] + [0] * max(0, n - len(row[:n])))

    print(count_clusters(matrix))


if __name__ == "__main__":
    main()
