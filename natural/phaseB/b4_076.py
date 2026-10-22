# snail climbs 7 by day, slips 3 at night, wall is 30
height = 0
day = 0
while True:
    day += 1
    height += 7
    if height >= 30:
        break
    height -= 3
print(day)
