for n in range(6, 25, 6):
    s = 0
    for d in range(1, n):
        if n % d == 0:
            s += d
    if s == n:
        print("perfect")
    elif s > n:
        print("abundant")
    else:
        print("deficient")
