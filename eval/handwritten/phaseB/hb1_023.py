limit = 55
for speed in range(50, 96, 9):
    over = speed - limit
    if over <= 0:
        print("ok")
    elif over < 10:
        print("warning")
    elif over < 25:
        print(over * 5)     # fine in dollars
    else:
        print("license suspended")
