# score table: points for each level, bonus for perfect levels
total = 0
for level in range(1, 8):
    points = level * 12
    misses = level % 3
    if misses == 0:
        points += 25
        print("perfect")
    elif misses == 1:
        points -= 5
    total += points
print(total)
