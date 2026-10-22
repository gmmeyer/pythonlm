# parking meter: quarters buy 15 minutes, but only 5 minutes after the first hour
minutes = 0
paid = 0
coins = 0
while minutes < 90:
    coins += 1
    paid += 25
    if minutes < 60:
        minutes += 15
    else:
        minutes += 5
print(coins)
print(minutes)
print(paid)
