# snail in a 10 m well: climbs 3 by day, slips 2 at night
height = 0
day = 0
while True:
    day += 1
    height += 3
    if height >= 10:
        break
    height -= 2
print(day)
print(height)
