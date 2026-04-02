def countSubmatrices(matrix, maxK):
    rows = len(matrix)
    cols = len(matrix[0])

    col_zero_count = [0] * cols
    col_prod = [1] * cols
    answer = 0
    limit = maxK + 1

    for i in range(rows):
        for j in range(cols):
            value = matrix[i][j]
            if value == 0:
                col_zero_count[j] += 1
            elif col_zero_count[j] == 0:
                if col_prod[j] > maxK or value > maxK or col_prod[j] > maxK // value:
                    col_prod[j] = limit
                else:
                    col_prod[j] *= value

        zero_in_prefix = 0
        prefix_prod = 1

        for j in range(cols):
            zero_in_prefix += col_zero_count[j]

            if zero_in_prefix > 0:
                answer += 1
            else:
                if col_prod[j] > maxK or prefix_prod > maxK or prefix_prod > maxK // col_prod[j]:
                    prefix_prod = limit
                else:
                    prefix_prod *= col_prod[j]

                if prefix_prod <= maxK:
                    answer += 1

    return answer


def main():
    rows, cols = map(int, input().split())
    matrix = [list(map(int, input().split())) for _ in range(rows)]
    maxK = int(input().strip())
    print(countSubmatrices(matrix, maxK))


if __name__ == "__main__":
    main()
