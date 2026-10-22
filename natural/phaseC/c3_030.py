for n in range(1, 9):
    if n == 4:
        roman = "IV"
    elif n >= 5:
        roman = "V" + "I" * (n - 5)
    else:
        roman = "I" * n
    print(n, roman)
