# parking lot with two levels
level1 = 0
level2 = 0
rejected = 0
for car in range(1, 31):
    if level1 < 8:
        level1 += 1
    elif level2 < 6:
        level2 += 1
    else:
        rejected += 1
print(level1)
print(level2)
print(rejected)
