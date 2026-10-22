# water tank: 4 litres in per minute, 3 litres out whenever the tap is open
level = 40
capacity = 60
tap_open = False
minute = 0
while minute < 30:
    minute += 1
    level += 4
    if level > capacity:
        level = capacity
    if level >= 55:
        tap_open = True
    if tap_open:
        level -= 7
        if level <= 30:
            tap_open = False
print(level)
print(tap_open)
