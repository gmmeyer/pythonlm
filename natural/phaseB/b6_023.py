target = 100
saved = 0
day = 0
coin = 3
while saved < target:
    day += 1
    saved += coin
    if day % 7 == 0:
        coin += 2
print(day)
print(saved)
print(coin)
