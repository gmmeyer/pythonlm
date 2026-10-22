# free trial for 14 days, then 2 per day
paid = 0
for day in range(1, 31):
    if day > 14:
        paid += 2
print(paid)
