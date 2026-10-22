daily_points = 23
used = 0
meal = 0
while True:
    meal += 1
    if meal == 1:
        cost = 5
    elif meal == 2:
        cost = 8
    else:
        cost = 4
    if used + cost > daily_points:
        print("skip it")
        break
    used += cost
    print(used)
print(meal - 1)
print(daily_points - used)
