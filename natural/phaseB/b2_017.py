# water tank filling and draining
level = 0
for minute in range(30):
    if minute < 10:
        level += 8
    elif minute < 20:
        level -= 3
    else:
        level += 1
    if level > 70:
        level = 70
print(level)
