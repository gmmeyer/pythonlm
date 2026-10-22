# A night guard patrols waypoints 0..6 back and forth. He turns around at
# both ends and spends an extra tick checking the door at waypoint 3.
# An intruder shows up at waypoint 5 from tick 15 on; the first time the
# guard stands there after that, the intruder is caught.
pos = 0
step = 1
tick = 0
waiting = 0
checks = 0
caught = False
print("night patrol")
while tick < 22:
    tick += 1
    if waiting > 0:
        waiting -= 1
        continue
    pos += step
    if pos == 6 or pos == 0:
        step = -step
        print("turn around at")
        print(pos)
    if pos == 3:
        waiting = 1
        checks += 1
    else:
        pass
    if tick >= 15 and pos == 5 and not caught:
        caught = True
        print("intruder caught at tick")
        print(tick)
print("door checks")
print(checks)
print(caught)
