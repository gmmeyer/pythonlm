# traffic light: 0 = green, 1 = yellow, 2 = red
state = 0
ticks = 0
cars = 0
for t in range(18):
    if state == 0:
        cars += 2
        if t % 4 == 3:
            state = 1
    elif state == 1:
        state = 2
    else:
        if t % 3 == 0:
            state = 0
    ticks += 1
print(state)
print(cars)
print(ticks)
