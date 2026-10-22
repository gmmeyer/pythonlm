# robot walking on a line
pos = 0
facing = 1
steps = 0
for cmd in range(1, 16):
    if cmd % 5 == 0:
        facing = -facing
    elif cmd % 2 == 1:
        pos += facing * 2
        steps += 1
    else:
        pos += facing
        steps += 1
print(pos)
print(steps)
print(facing)
