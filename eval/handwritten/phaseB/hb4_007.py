# A robot on a 7x7 grid. Its program is the digits of a number read from
# the lowest digit: 1 = north, 2 = east, 3 = south, 4 = west. Two programs
# alternate. The robot refuses to step off the grid and counts bumps.
x = 3
y = 3
bumps = 0
moves = 0
print("robot start")
for rep in range(4):
    if rep % 2 == 0:
        prog = 221
    else:
        prog = 334
    while prog > 0:
        d = prog % 10
        prog //= 10
        nx = x
        ny = y
        if d == 1:
            ny += 1
        elif d == 2:
            nx += 1
        elif d == 3:
            ny -= 1
        else:
            nx -= 1
        if 0 <= nx <= 6 and 0 <= ny <= 6:
            x = nx
            y = ny
            moves += 1
        else:
            bumps += 1
    print("after program")
    print(x)
    print(y)
print("moves and bumps")
print(moves)
print(bumps)
