for n in range(100, 1000, 150):
    s = n // 100 + n // 10 % 10 + n % 10
    if 0 < s < 5:
        print("small")
    elif 5 <= s <= 10:
        print("medium")
    else:
        print("large")
