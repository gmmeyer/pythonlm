days_late = 12
fine = 0
for day in range(1, days_late + 1):
    if day <= 3:
        fine += 1
    else:
        fine += 2
    if fine >= 15:
        fine = 15
        break
print(fine)
