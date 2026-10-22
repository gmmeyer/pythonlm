# round robin between 4 teams: win 3, draw 1, loss 0
points = 0
for other in range(1, 4):
    diff = (other * 7 + 2) % 5 - 2
    if diff > 0:
        points += 3
    elif diff == 0:
        points += 1
print(points)
