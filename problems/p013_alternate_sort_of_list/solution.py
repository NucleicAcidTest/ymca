import sys


def alternate_sort(values):
    values.sort()
    return values[::2]


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    arr = data[1:1 + n]
    result = alternate_sort(arr)
    print(" ".join(map(str, result)))


if __name__ == "__main__":
    main()
