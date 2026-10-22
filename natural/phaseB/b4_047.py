weekdays = 0
weekends = 0
for day in range(1, 8):
    if day == 6 or day == 7:
        weekends += 1
    else:
        weekdays += 1
print(weekdays)
print(weekends)
