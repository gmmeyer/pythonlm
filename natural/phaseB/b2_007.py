# thermostat
temp = 15
target = 21
heater = False
on_count = 0
for hour in range(24):
    if temp < target - 1:
        heater = True
    elif temp > target + 1:
        heater = False
    if heater:
        temp += 2
        on_count += 1
    else:
        temp -= 1
print(temp)
print(on_count)
print(heater)
