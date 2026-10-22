# toll booth: 2 axles pay 4, 3 axles pay 7, more pay 12
revenue = 0
trucks = 0
for car in range(1, 16):
    axles = 2 + car % 4
    if axles == 2:
        revenue += 4
    elif axles == 3:
        revenue += 7
    else:
        revenue += 12
        if axles >= 5:
            trucks += 1
print(revenue)
print(trucks)
