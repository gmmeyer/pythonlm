# Nim with three heaps between two fixed strategies.
# Player A takes up to three stones from the largest heap.
# Player B takes one stone from the first heap that is not empty.
# Whoever takes the last stone wins.
h1 = 7
h2 = 5
h3 = 9
player = 0
turns = 0
print("nim begins")
while h1 + h2 + h3 > 0:
    turns += 1
    if player == 0:
        if h1 >= h2 and h1 >= h3:
            take = 3
            if h1 < 3:
                take = h1
            h1 -= take
        elif h2 >= h3:
            take = 3
            if h2 < 3:
                take = h2
            h2 -= take
        else:
            take = 3
            if h3 < 3:
                take = h3
            h3 -= take
    else:
        if h1 > 0:
            h1 -= 1
        elif h2 > 0:
            h2 -= 1
        else:
            h3 -= 1
    print(h1 * 100 + h2 * 10 + h3)
    player = 1 - player
print("turns played")
print(turns)
if player == 1:
    print("A wins")
else:
    print("B wins")
