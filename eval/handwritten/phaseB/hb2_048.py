for m in range(3, 8, 4):
    a = 0
    b = 1
    k = 0
    while True:
        a, b = b, (a + b) % m
        k += 1
        if a == 0 and b == 1:
            break
    print(k)
