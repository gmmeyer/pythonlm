board = "XXXOOXOXO"
for r in range(3):
    row = ""
    for c in range(3):
        row += board[r * 3 + c]
    print(row)
    if row == "XXX":
        print("X wins on row", r)
    elif row == "OOO":
        print("O wins on row", r)
