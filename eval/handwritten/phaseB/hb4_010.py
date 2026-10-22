# A thermostat with hysteresis: the heater switches on below 18 degrees
# and off above 22. The heater adds 2 degrees per tick, while the cold
# outside removes more heat every ten ticks.
temp = 20
heater = False
outside_drop = 1
switches = 0
print("thermostat log")
for t in range(27):
    if heater:
        temp += 2
    temp -= outside_drop
    if t % 10 == 9:
        outside_drop += 1
        print("colder outside")
    if not heater and temp < 18:
        heater = True
        switches += 1
        print("heater on")
        print(temp)
    elif heater and temp > 22:
        heater = False
        switches += 1
        print("heater off")
        print(temp)
print("switches")
print(switches)
print(heater)
print(temp)
