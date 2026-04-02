def smallestPermutation(num):
    if num == 0:
        return 0

    if num > 0:
        digits = list(str(num))
        digits.sort()

        first_non_zero = 0
        while first_non_zero < len(digits) and digits[first_non_zero] == "0":
            first_non_zero += 1

        result = [digits[first_non_zero]]
        result.extend(digits[:first_non_zero])
        result.extend(digits[first_non_zero + 1:])
        return int("".join(result))

    digits = list(str(-num))
    digits.sort(reverse=True)
    return -int("".join(digits))


def main():
    num = int(input().strip())
    print(smallestPermutation(num))


if __name__ == "__main__":
    main()
