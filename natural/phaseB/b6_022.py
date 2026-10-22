# traffic light: green 5, yellow 2, red 6 ticks
state = 0
timer = 0
green_ticks = 0
for tick in range(39):
    if state == 0:
        green_ticks += 1
        if timer == 4:
            state = 1
            timer = -1
    elif state == 1:
        if timer == 1:
            state = 2
            timer = -1
    else:
        if timer == 5:
            state = 0
            timer = -1
    timer += 1
print(green_ticks)
print(state)
