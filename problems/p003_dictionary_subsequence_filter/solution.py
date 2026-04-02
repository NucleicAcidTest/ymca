from bisect import bisect_right


def is_subsequence(word, positions):
    current_index = -1

    for ch in word:
        if ch not in positions:
            return False

        char_positions = positions[ch]
        next_pos_idx = bisect_right(char_positions, current_index)
        if next_pos_idx == len(char_positions):
            return False
        current_index = char_positions[next_pos_idx]

    return True


def find_words(master, dictionary):
    positions = {}
    for idx, ch in enumerate(master):
        positions.setdefault(ch, []).append(idx)

    result = []
    for word in dictionary:
        if is_subsequence(word, positions):
            result.append(word)

    return result


def main():
    master = input().strip()
    n = int(input().strip())
    dictionary = input().strip().split()

    # Respect the declared size even if the input line contains extra tokens.
    dictionary = dictionary[:n]

    result = find_words(master, dictionary)
    if result:
        print(" ".join(result))
    else:
        print(-1)


if __name__ == "__main__":
    main()
