# basketball: lead changes over 8 scoring plays
home = 0
away = 0
leader = 0
changes = 0
for play in range(1, 9):
    if play % 3 == 0:
        away += 3
    elif play % 2 == 0:
        home += 2
    else:
        home += 1
        away += 2
    if home > away:
        now = 1
    elif away > home:
        now = -1
    else:
        now = 0
    if now != 0 and leader != 0 and now != leader:
        changes += 1
    if now != 0:
        leader = now
print(home)
print(away)
print(changes)
