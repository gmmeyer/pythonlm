# flood warning after 3 days in a row with more than 10 mm of rain
streak = 0
warning_day = 0
for day in range(1, 15):
    rain = day * 7 % 31
    if rain > 10:
        streak += 1
    else:
        streak = 0
    if streak == 3 and warning_day == 0:
        warning_day = day
print(warning_day)
print(streak)
