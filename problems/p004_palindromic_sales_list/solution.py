def palindromicSalesList(salesData):
    left = 0
    right = len(salesData) - 1
    front = []
    back = []

    while left < right:
        i = left
        j = right
        left_sum = salesData[i]
        right_sum = salesData[j]

        while i < j and left_sum != right_sum:
            if left_sum < right_sum:
                i += 1
                left_sum += salesData[i]
            else:
                j -= 1
                right_sum += salesData[j]

        if i >= j:
            return front + [sum(salesData[left:right + 1])] + back[::-1]

        front.append(left_sum)
        back.append(right_sum)
        left = i + 1
        right = j - 1

    if left == right:
        return front + [salesData[left]] + back[::-1]

    return front + back[::-1]


def main():
    salesData_size = int(input().strip())
    salesData = list(map(int, input().split()))
    salesData = salesData[:salesData_size]

    result = palindromicSalesList(salesData)
    print(" ".join(map(str, result)))


if __name__ == "__main__":
    main()
