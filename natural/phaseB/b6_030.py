# happy hour is 16:00-18:00; drinks cost half
total = 0
for hour in range(12, 22, 2):
    if hour >= 16 and hour < 18:
        total += 4
    else:
        total += 8
print(total)
