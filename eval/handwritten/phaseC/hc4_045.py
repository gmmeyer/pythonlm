# A knight wanders a chessboard. Each step tries a move picked by the
# step number and skips it when it would leave the board.
files = "abcdefgh"
x = 1
y = 0
path = files[x] + str(y + 1)
for step in range(10):
    k = step % 4
    if k == 0:
        dx = 1
        dy = 2
    elif k == 1:
        dx = 2
        dy = 1
    elif k == 2:
        dx = -2
        dy = 1
    else:
        dx = -2
        dy = -1
    nx = x + dx
    ny = y + dy
    if nx < 0 or nx > 7 or ny < 0 or ny > 7:
        print("step", step, "blocked")
        continue
    x = nx
    y = ny
    print("step", step, "->", files[x] + str(y + 1))
    if len(path) < 40:
        path = path + " " + files[x] + str(y + 1)
print(path)
