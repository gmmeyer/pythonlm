for r in range(4):
    row = ""
    for c in range(8):
        if (r + c) % 2 == 0:
            row += "#"
        else:
            row += "."
    print(row)
