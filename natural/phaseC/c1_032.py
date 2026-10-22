# daily highs as bars
temp = 12
for day in range(1, 8):
    print("Day", day, "|" + "*" * temp)
    if day % 2 == 0:
        temp += 3
    else:
        temp -= 1
