battery = 100
charging = False
cycles = 0
for hour in range(40):
    if charging:
        battery += 15
        if battery >= 100:
            battery = 100
            charging = False
    else:
        battery -= 9
        if battery <= 20:
            charging = True
            cycles += 1
print(battery)
print(cycles)
