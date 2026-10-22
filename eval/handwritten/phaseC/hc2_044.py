for n in range(5, 40, 9):
    b = ""
    m = n
    ones = 0
    while m > 0:
        if m % 2 == 1:
            ones += 1
        b = str(m % 2) + b
        m //= 2
    print(n, b + str(ones % 2), sep=": ")
