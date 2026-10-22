# Traffic light controller: 0 = green, 1 = yellow, 2 = red.
# Each state has its own duration. A pedestrian button pressed on every
# seventh tick cuts the green phase short (but green lasts at least 2 ticks).
state = 0
timer = 0
green_time = 5
yellow_time = 2
red_time = 4
cycles = 0
tick = 0
print("traffic light start")
while cycles < 2:
    tick += 1
    timer += 1
    button = tick % 7 == 0
    if state == 0:
        if timer >= green_time or (button and timer >= 2):
            state = 1
            timer = 0
            print("green -> yellow")
            print(tick)
    elif state == 1:
        if timer >= yellow_time:
            state = 2
            timer = 0
            print("yellow -> red")
    else:
        if timer >= red_time:
            state = 0
            timer = 0
            cycles += 1
            print("red -> green")
            print(cycles)
print("total ticks")
print(tick)
