# The dice game Pig. On a turn a player keeps rolling and adds to a turn
# total, but a roll of 1 wipes the turn total and ends the turn.
# Hana holds once her turn total reaches 8; Ivo holds at 5.
# Rolls come from x = (x * 7 + 3) % 101, die = x % 6 + 1. First to 20 wins.
x = 4
hana = 0
ivo = 0
player = 0
turn_total = 0
print("pig")
while hana < 20 and ivo < 20:
    x = (x * 7 + 3) % 101
    die = x % 6 + 1
    if die == 1:
        turn_total = 0
        player = 1 - player
        print("pig out")
        continue
    turn_total += die
    if player == 0 and turn_total >= 8:
        hana += turn_total
        turn_total = 0
        player = 1
        print(hana)
    elif player == 1 and turn_total >= 5:
        ivo += turn_total
        turn_total = 0
        player = 0
        print(ivo)
if hana >= 20:
    print("hana wins")
else:
    print("ivo wins")
