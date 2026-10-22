# stopwatch: a lap is recorded whenever the button is pressed
last = 0
laps = 0
fastest = 999
for second in range(1, 61):
    if second % 12 == 0 or second % 17 == 0:
        lap_time = second - last
        last = second
        laps += 1
        if lap_time < fastest:
            fastest = lap_time
print(laps)
print(fastest)
