c = 0
for x in range(1, 7):
    if x % 3 == 0:
        continue
    for y in range(x, 21):
        if x * y > 20:
            break
        if (x + y) % 2 == 0:
            c += 1
print(c)
