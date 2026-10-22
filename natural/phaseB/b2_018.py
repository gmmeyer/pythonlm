# battery drain with charging flag
battery = 100
charging = False
low_events = 0
for hour in range(1, 25):
    if charging:
        battery += 15
        if battery >= 80:
            charging = False
    else:
        battery -= 9
        if battery <= 20:
            charging = True
            low_events += 1
print(battery)
print(low_events)
print(charging)
