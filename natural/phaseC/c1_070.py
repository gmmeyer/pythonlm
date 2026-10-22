# bouncing ball in a corridor
pos = 2
way = 1
for t in range(14):
    print("|" + " " * pos + "o" + " " * (9 - pos) + "|")
    pos += way
    if pos == 9 or pos == 0:
        way = -way
