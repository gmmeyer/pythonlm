# checkout line: one cashier, two customers a minute
waiting = 0
served = 0
for minute in range(1, 13):
    if minute <= 5:
        waiting += 3       # lunch rush
    elif minute % 2 == 0:
        waiting += 1
    if waiting > 0:
        take = 2
        if waiting < 2:
            take = waiting
        waiting -= take
        served += take
    print(waiting)
print(served)
