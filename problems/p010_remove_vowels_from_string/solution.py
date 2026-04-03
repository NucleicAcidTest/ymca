def main():
    houses = input().strip()
    vowels = set[str]("aeiouAEIOU")
    result = "".join(char for char in houses if char not in vowels)
    print(result)


if __name__ == "__main__":
    main()
