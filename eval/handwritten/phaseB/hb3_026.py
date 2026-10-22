for t in range(-3, 12, 3):
    if t < 0:
        print(-1)
    elif 0 <= t < 3:
        print(0)
    elif 3 <= t < 6:
        if t % 2:
            print(31)
        else:
            print(30)
    elif t == 6 or t == 7:
        print(6)
    else:
        print(9)
