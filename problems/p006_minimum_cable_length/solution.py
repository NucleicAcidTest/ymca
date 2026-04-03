import sys


def minimum_cable_length(state, dist):
    n = len(state)
    on_indices = [i for i, value in enumerate(state) if value == 1]

    first_on = on_indices[0]
    last_on = on_indices[-1]
    answer = 0

    if first_on > 0:
        answer += dist[first_on] - dist[0]

    if last_on < n - 1:
        answer += dist[-1] - dist[last_on]

    for left, right in zip(on_indices, on_indices[1:]):
        total_span = dist[right] - dist[left]
        max_gap = 0

        for i in range(left + 1, right + 1):
            gap = dist[i] - dist[i - 1]
            if gap > max_gap:
                max_gap = gap

        answer += total_span - max_gap

    return answer


def parse_input():
    tokens = list(map(int, sys.stdin.buffer.read().split()))
    if not tokens:
        return [], []

    pos = 0
    state_size = tokens[pos]
    pos += 1
    state = tokens[pos:pos + state_size]
    pos += state_size

    remaining = len(tokens) - pos
    if remaining == state_size:
        dist = tokens[pos:pos + state_size]
        return state, dist

    dist_size = tokens[pos]
    pos += 1
    dist = tokens[pos:pos + dist_size]
    return state, dist[:state_size]


def main():
    state, dist = parse_input()
    if not state:
        return
    print(minimum_cable_length(state, dist))


if __name__ == "__main__":
    main()
