# thermostat with a heating band
temp = 12
for hour in range(10):
    if temp < 18:
        temp += 3
    elif temp > 22:
        temp -= 2
    else:
        temp -= 1
    print(temp)
