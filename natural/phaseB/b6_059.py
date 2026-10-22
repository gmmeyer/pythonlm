# trash pickup on days 2 and 5 of each week; count pickups in 4 weeks
pickups = 0
weekend_days = 0
for day in range(28):
    d = day % 7 + 1
    if d == 2 or d == 5:
        pickups += 1
    if d >= 6:
        weekend_days += 1
print(pickups)
print(weekend_days)
