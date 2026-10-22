# thermostat: heater on below 18, off above 22
temp = 20
heater = False
switches = 0
for hour in range(24):
    if heater:
        temp += 2
    else:
        temp -= 1
    if temp < 18 and not heater:
        heater = True
        switches += 1
    elif temp > 22 and heater:
        heater = False
        switches += 1
print(temp)
print(heater)
print(switches)
