temp = 18
print("day", "temp", "chart", sep=" | ")
for day in range(1, 8):
    print(day, temp, "o" * (temp // 2), sep=" | ")
    if day % 3 == 0:
        temp -= 4
    else:
        temp += 2
