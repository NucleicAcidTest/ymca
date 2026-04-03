import heapq


def solve():
    n = int(input().strip())
    dist = list(map(int, input().split()))
    juice = list(map(int, input().split()))
    d, k = map(int, input().split())

    stalls = sorted(zip(dist, juice))
    stalls.append((d, 0))

    heap = []
    prev = 0
    fuel = k
    stops = 0

    for pos, gain in stalls:
        fuel -= pos - prev

        while fuel < 0 and heap:
            fuel += -heapq.heappop(heap)
            stops += 1

        if fuel < 0:
            print(-1)
            return

        heapq.heappush(heap, -gain)
        prev = pos

    print(stops)


if __name__ == "__main__":
    solve()
