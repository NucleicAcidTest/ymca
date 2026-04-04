def next_state(state):
    n = len(state)
    return [
        (state[i - 1] if i > 0 else 0) ^ (state[i + 1] if i + 1 < n else 0)
        for i in range(n)
    ]


def parse_input():
    first = input().strip()
    second = input().strip()

    if set(second) <= {"0", "1"} and " " not in second:
        days = int(first)
        state = [int(ch) for ch in second]
        return state, days

    n = int(first)
    state = list(map(int, second.split()))
    if len(state) < n:
        extra = list(map(int, input().split()))
        state.extend(extra)
    state = state[:n]
    days = int(input().strip())
    return state, days


def solve():
    state, days = parse_input()

    seen = {}
    order = []
    step = 0

    while step < days:
        key = tuple(state)
        if key in seen:
            start = seen[key]
            cycle_len = step - start
            state = order[start + (days - start) % cycle_len]
            break

        seen[key] = step
        order.append(state[:])
        state = next_state(state)
        step += 1

    print(" ".join(map(str, state)))


if __name__ == "__main__":
    solve()
