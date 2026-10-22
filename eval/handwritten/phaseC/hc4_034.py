# Tic-tac-toe on a nine-character board string. A move rebuilds the
# string one character at a time, swapping in the mark at its square.
board = "........."
for t in range(5):
    if t == 0:
        p = 4
    elif t == 1:
        p = 0
    elif t == 2:
        p = 2
    elif t == 3:
        p = 6
    else:
        p = 3
    if t % 2 == 0:
        mark = "X"
    else:
        mark = "O"
    nb = ""
    for k in range(9):
        if k == p:
            nb += mark
        else:
            nb += board[k]
    board = nb
print(board[0] + board[1] + board[2])
print(board[3] + board[4] + board[5])
print(board[6] + board[7] + board[8])
print("board string:", board)
