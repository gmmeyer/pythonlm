# a bulb lasts 12 hours; how many bulbs for 50 hours of use?
bulbs = 1
life = 0
hour = 0
while hour < 50:
    hour += 1
    life += 1
    if life == 12 and hour < 50:
        bulbs += 1
        life = 0
print(bulbs)
print(life)
