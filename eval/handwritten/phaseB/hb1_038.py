# distances in units of 100 m; one lap of the track is 4 units
goal = 50
covered = 0
minutes = 0
lap = 0
while covered < goal:
    lap += 1
    covered += 4
    if lap % 4 == 0:
        minutes += 4    # walk every fourth lap
        continue
    minutes += 2
print(lap)
print(minutes)
print(covered - goal)
