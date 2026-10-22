# Subtraction game: 31 counters, each turn removes 1 to 4, and whoever
# takes the last counter wins. Alice plays perfectly (she leaves a multiple
# of 5 when she can); Bert simply copies Alice's previous move.
counters = 31
last = 2
turn = 0
print("take away game")
while counters > 0:
    if turn == 0:
        take = counters % 5
        if take == 0:
            take = 1
    else:
        take = last
        if take > counters:
            take = counters
    counters -= take
    last = take
    if turn == 0:
        print("alice takes")
    else:
        print("bert takes")
    print(take)
    turn = 1 - turn
if turn == 1:
    print("alice wins")
else:
    print("bert wins")
