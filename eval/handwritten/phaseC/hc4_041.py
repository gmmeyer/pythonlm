# Dice faces 1..6 drawn as 3x3 grids of pips ('o') inside a frame.
for v in range(1, 7):
    corner = " "
    side = " "
    mid = " "
    if v >= 4:
        side = "o"
    if v >= 2:
        corner = "o"
    if v % 2 == 1:
        mid = "o"
    if v == 6:
        row2 = "o" + " " + "o"
    else:
        row2 = " " + mid + " "
    print("+---+", v)
    print("|" + corner + " " + side + "|")
    print("|" + row2 + "|")
    print("|" + side + " " + corner + "|")
print("+---+")
