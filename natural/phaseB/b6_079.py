# the sauna keeps its heat between 70 and 90 degrees
temp = 60
heater = True
switches = 0
for minute in range(40):
    if heater:
        temp += 4
    else:
        temp -= 3
    if heater and temp >= 90:
        heater = False
        switches += 1
    elif not heater and temp <= 70:
        heater = True
        switches += 1
print(temp)
print(switches)
print(heater)
