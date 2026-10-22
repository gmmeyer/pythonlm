# Two racers take turns rolling a pseudo-random die
# (x = (x * 7 + 3) % 101, die = x % 6 + 1) on a 24-square track.
# A six earns 2 bonus squares; landing on 11 or 19 sends you back 5.
x = 9
p1 = 0
p2 = 0
turn = 1
print("dice race")
while p1 < 24 and p2 < 24:
    x = (x * 7 + 3) % 101
    die = x % 6 + 1
    if die == 6:
        die += 2
    if turn == 1:
        p1 += die
        if p1 == 11 or p1 == 19:
            p1 -= 5
            print("p1 slides back")
        print(p1)
    else:
        p2 += die
        if p2 == 11 or p2 == 19:
            p2 -= 5
            print("p2 slides back")
        print(p2)
    turn = 3 - turn
if p1 >= 24:
    print("player one wins")
else:
    print("player two wins")
