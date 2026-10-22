hits = 0
for v in range(-5, 6):
    if -2 <= v < 3:
        hits += 2
    elif v < -2 or v >= 4:
        hits -= 1
    else:
        hits += 100
print(hits)
print(v)
