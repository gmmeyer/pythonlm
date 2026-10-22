# thermostat schedule over one day
temp = 17
heater_hours = 0
for hour in range(24):
    if 6 <= hour < 9 or 17 <= hour < 22:
        target = 21
    elif hour >= 22 or hour < 6:
        target = 16
    else:
        target = 18
    if temp < target:
        temp += 1
        heater_hours += 1
    elif temp > target:
        temp -= 1
print(heater_hours)
print(temp)
