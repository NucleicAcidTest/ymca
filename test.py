def main():
    try:
        S, K = map(int, input().split())
        s = input().strip()
    except Exception:
        return
    left = 0
    zero_count = 0
    max_len = 0

    for right in range(S):
        if s[right] == '0':
            zero_count += 1
        while zero_count > K:
            if s[left] == '0':
                zero_count -= 1
            left += 1
        max_len = max(max_len, right - left + 1)

    if max_len == 0:
        print(1)
        return
    ans = 0
    has_empty_set = False
    zero_count = 0
    for i in range(max_len):
        if s[i] == '0':
            zero_count += 1

    if zero_count <= K:
        if zero_count == 0:
            has_empty_set = True
        else:
            ans += 1
    for i in range(1, S - max_len + 1):
        if s[i - 1] == '0':
            zero_count -= 1
        if s[i + max_len - 1] == '0':
            zero_count += 1

        if zero_count <= K:
            if zero_count == 0:
                has_empty_set = True
            else:
                ans += 1
    if has_empty_set:
        ans += 1

    print(ans)

if __name__ == '__main__':
    main()