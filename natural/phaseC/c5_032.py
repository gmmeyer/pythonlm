board = "xoxoxxo"
bad = -1
for i in range(1, len(board)):
    if board[i] == board[i - 1] and bad == -1:
        bad = i
if bad == -1:
    print("moves alternate")
else:
    print("player", board[bad], "moved twice at move", bad + 1)
