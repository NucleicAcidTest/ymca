import sys
from collections import deque


def find_max_ceos(person_ids):
    n = len(person_ids)
    indegree = [0] * n
    for favorite in person_ids:
        indegree[favorite] += 1

    longest_chain = [1] * n
    queue = deque(i for i in range(n) if indegree[i] == 0)

    while queue:
        node = queue.popleft()
        nxt = person_ids[node]
        if longest_chain[node] + 1 > longest_chain[nxt]:
            longest_chain[nxt] = longest_chain[node] + 1
        indegree[nxt] -= 1
        if indegree[nxt] == 0:
            queue.append(nxt)

    max_cycle = 0
    pair_sum = 0
    visited = [False] * n

    for i in range(n):
        if indegree[i] <= 0 or visited[i]:
            continue

        cycle_nodes = []
        current = i
        while not visited[current]:
            visited[current] = True
            cycle_nodes.append(current)
            current = person_ids[current]

        cycle_len = len(cycle_nodes)
        if cycle_len == 2:
            a, b = cycle_nodes
            pair_sum += longest_chain[a] + longest_chain[b]
        elif cycle_len > max_cycle:
            max_cycle = cycle_len

    return max(max_cycle, pair_sum)


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    person_ids = data[1:1 + n]
    print(find_max_ceos(person_ids))


if __name__ == "__main__":
    main()
