def minimumCableLength(state, dist):
    n = len(state)
    on_indices = [i for i, value in enumerate(state) if value == 1]

    first_on = on_indices[0]
    last_on = on_indices[-1]
    answer = 0

    if first_on > 0:
        answer += dist[first_on] - dist[0]

    if last_on < n - 1:
        answer += dist[-1] - dist[last_on]

    for idx in range(len(on_indices) - 1):
        left = on_indices[idx]
        right = on_indices[idx + 1]

        if right == left + 1:
            continue

        total_span = dist[right] - dist[left]
        max_gap = 0

        for i in range(left, right):
            gap = dist[i + 1] - dist[i]
            if gap > max_gap:
                max_gap = gap

        answer += total_span - max_gap

    return answer


def main():
    num = int(input().strip())
    state = list(map(int, input().split()))
    dist = list(map(int, input().split()))

    state = state[:num]
    dist = dist[:num]

    print(minimumCableLength(state, dist))


if __name__ == "__main__":
    main()
