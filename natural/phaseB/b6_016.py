# overtime: hours past 8 in a day are paid at time and a half (rate 10)
pay = 0
for day in range(1, 6):
    hours = 6 + day * 2 % 5
    if hours > 8:
        pay += 8 * 10 + (hours - 8) * 15
    else:
        pay += hours * 10
print(pay)
