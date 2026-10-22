# stock levels of two items
apples = 30
pears = 12
day = 0
while apples > 0 and pears > 0:
    day += 1
    apples -= 4
    pears -= 2
    if day == 3:
        pears += 6
print(day)
print(apples)
print(pears)
