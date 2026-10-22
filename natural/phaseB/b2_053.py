# traffic light as an int state with a cars-waiting counter
state = 2
waiting = 0
passed = 0
for tick in range(24):
    waiting += 1
    if state == 0:
        if waiting > 0:
            waiting -= 2
            passed += 2
            if waiting < 0:
                waiting = 0
    if tick % 6 == 5:
        state = 0
    elif tick % 6 == 3:
        state = 2
print(waiting)
print(passed)
print(state)
