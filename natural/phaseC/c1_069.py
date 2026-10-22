pos = 0
step = 1
for i in range(16):
    print(" " * pos + "*")
    pos += step
    if pos == 8 or pos == 0:
        step = -step
