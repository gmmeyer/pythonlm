# a 5x5 grid showing only the cells where the product is a square-ish value
for i in range(1, 6):
    for j in range(1, 6):
        p = i * j
        if p == 4 or p == 9 or p == 16 or p == 25:
            print(p)
    print("row")
