c = 0
for y in range(300, 421, 4):
    if y % 100 != 0 or y % 400 == 0:
        c += 1
print(c)
print(c == 30)
