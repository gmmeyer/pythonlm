# tennis game: first to 4 points, win by 2; points won by whoever the rule says
a = 0
b = 0
rally = 0
winner = 0
while winner == 0:
    rally += 1
    if rally % 3 == 0:
        b += 1
    else:
        a += 1
    if a >= 4 and a - b >= 2:
        winner = 1
    elif b >= 4 and b - a >= 2:
        winner = 2
print(a)
print(b)
print(winner)
