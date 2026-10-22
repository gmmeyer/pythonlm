leaps = 0
for year in range(380, 420):
    if year % 400 == 0:
        leaps += 1
    elif year % 100 == 0:
        pass
    elif year % 4 == 0:
        leaps += 1
print(leaps)
