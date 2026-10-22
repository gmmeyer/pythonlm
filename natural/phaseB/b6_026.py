# data plan: 150 MB a month; usage grows each day
used = 0
over_days = 0
for day in range(1, 21):
    used += 10 + day
    if used > 150:
        over_days += 1
print(used)
print(over_days)
print(used > 150)
