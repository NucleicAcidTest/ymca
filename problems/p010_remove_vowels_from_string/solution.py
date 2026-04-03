VOWELS = set("aeiouAEIOU")


def removeVowels(engStr: str) -> str:
    return "".join(ch for ch in engStr if ch not in VOWELS)


def main() -> None:
    engStr = input().rstrip("\n")
    print(removeVowels(engStr))


if __name__ == "__main__":
    main()
