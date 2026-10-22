for n in range(24, 33, 4):
    s = 0
    for d in range(1, n // 2 + 1):
        if n % d == 0:
            s += d
    if s == n:
        print('perfect')
    elif s > n:
        print('abundant')
    else:
        print('deficient')
