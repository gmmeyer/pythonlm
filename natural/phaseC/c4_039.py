for a in range(1, 5):
    row = ""
    for b in range(1, 6):
        p = a * b
        row += " " * (3 - len(str(p))) + str(p)
    print(row)
