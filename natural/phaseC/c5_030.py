for row in range(4):
    line = ""
    for col in range(8):
        if (row + col) % 2 == 0:
            line += "#"
        else:
            line += "."
    print(line)
