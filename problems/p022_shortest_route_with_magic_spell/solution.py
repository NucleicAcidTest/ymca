import heapq


def main():
    n, m, start, end, limit = map(int, input().split())
    limit = min(limit, n)

    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))
        graph[v].append((u, w))

    inf = float("inf")
    dist = [[inf] * (limit + 1) for _ in range(n)]
    dist[start][0] = 0
    heap = [(0, start, 0)]

    while heap:
        cur_dist, city, used = heapq.heappop(heap)
        if cur_dist > dist[city][used]:
            continue

        if city == end:
            print(cur_dist)
            return

        for nxt, weight in graph[city]:
            paid = cur_dist + weight
            if paid < dist[nxt][used]:
                dist[nxt][used] = paid
                heapq.heappush(heap, (paid, nxt, used))

            if used < limit and cur_dist < dist[nxt][used + 1]:
                dist[nxt][used + 1] = cur_dist
                heapq.heappush(heap, (cur_dist, nxt, used + 1))

    print(-1)


def solve():
    main()


if __name__ == "__main__":
    main()
