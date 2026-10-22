# coffee card: buy 9, the 10th is free
stamps = 0
paid = 0
free = 0
for coffee in range(1, 26):
    if stamps == 9:
        free += 1
        stamps = 0
        continue
    stamps += 1
    paid += 4
print(free)
print(paid)
