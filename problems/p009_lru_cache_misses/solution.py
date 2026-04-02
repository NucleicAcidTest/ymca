from collections import OrderedDict


def countCacheMisses(pages, size):
    if size == 0:
        return len(pages)

    cache = OrderedDict()
    misses = 0

    for page in pages:
        if page in cache:
            cache.move_to_end(page)
            continue

        misses += 1
        if len(cache) == size:
            cache.popitem(last=False)
        cache[page] = True

    return misses


def main():
    inputNum_size = int(input().strip())
    pages = list(map(int, input().split()))
    size = int(input().strip())

    pages = pages[:inputNum_size]
    print(countCacheMisses(pages, size))


if __name__ == "__main__":
    main()
