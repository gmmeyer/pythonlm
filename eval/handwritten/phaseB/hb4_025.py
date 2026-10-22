# A snail climbs out of a 40-unit well. By day it climbs 7, by night it
# slides back 4. On rainy days (every fifth day) it only manages 3.
depth = 40
height = 0
day = 0
print("snail in a well")
while True:
    day += 1
    if day % 5 == 0:
        height += 3
        print("rain")
    else:
        height += 7
    if height >= depth:
        print("out on day")
        print(day)
        break
    height -= 4
    print(height)
print(height - depth)
