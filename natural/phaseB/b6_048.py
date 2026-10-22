# chess clock: white has 30 seconds and black has 25, moves cost more over time
white = 30
black = 25
turn = 0
move = 0
flagged = False
while not flagged:
    move += 1
    spend = 2 + move // 4
    if turn == 0:
        white -= spend
        if white <= 0:
            flagged = True
        turn = 1
    else:
        black -= spend
        if black <= 0:
            flagged = True
        turn = 0
print(move)
if white <= 0:
    print("white flagged")
else:
    print("black flagged")
