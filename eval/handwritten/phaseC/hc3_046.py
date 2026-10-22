row = "#." * 4
for r in range(4):
    line = ""
    for c in range(8):
        line = line + row[(r + c) % 2]
    print(line, line == row, line[-1])
