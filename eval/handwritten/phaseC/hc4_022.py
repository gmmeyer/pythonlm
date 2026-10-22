# A zigzag line bouncing between two walls, one row per tick.
width = 6
pos = 0
step = 1
for t in range(16):
    print("|" + " " * pos + "*" + " " * (width - pos) + "|", t)
    pos += step
    if pos == width or pos == 0:
        step = -step
print("+" + "-" * (width + 1) + "+")
