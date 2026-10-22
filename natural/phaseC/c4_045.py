stock = 20
day = 0
while stock >= 5:
    day += 1
    stock -= day * 3
    print("day", day, "stock", stock)
    if stock < 5:
        print("restock needed on day", day)
