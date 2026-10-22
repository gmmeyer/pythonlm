# day numbers: 1 = Monday ... 7 = Sunday
gym_days = 0
for day in range(1, 8):
    if day == 6 or day == 7:
        print("sleep in")
        continue
    if day % 2 == 1:
        print("gym")
        gym_days += 1
    else:
        print("swim")
print(gym_days)
