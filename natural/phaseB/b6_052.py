# hand back change in 20s, 10s, 5s and 1s
change = 87
twenties = 0
tens = 0
fives = 0
ones = 0
while change > 0:
    if change >= 20:
        change -= 20
        twenties += 1
    elif change >= 10:
        change -= 10
        tens += 1
    elif change >= 5:
        change -= 5
        fives += 1
    else:
        change -= 1
        ones += 1
print(twenties)
print(tens)
print(fives)
print(ones)
