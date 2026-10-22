# checkerboard
rows = 6
cols = 8
for r in range(rows):
    line = ""
    for c in range(cols):
        if (r + c) % 2 == 0:
            line = line + "#"
        else:
            line = line + "."
    print(line)
