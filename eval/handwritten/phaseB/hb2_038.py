for n in range(11, 20, 2):
    if n % 5 == 0:
        continue
    r = 10 % n
    k = 1
    while r != 1:
        r = r * 10 % n
        k += 1
    print(k)
