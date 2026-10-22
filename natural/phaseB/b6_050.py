# car rental: 30 a day, but the 7th day of a week is free
days = 10
cost = 0
for d in range(1, days + 1):
    if d % 7 != 0:
        cost += 30
print(cost)
