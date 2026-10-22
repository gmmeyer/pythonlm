# game: reach 100 points using steps of 15, 20 or 9
points = 0
turn = 0
while points < 100:
    turn += 1
    if turn % 3 == 1:
        points += 15
    elif turn % 3 == 2:
        points += 20
    else:
        points += 9
print(turn)
print(points)
print(points - 100)
