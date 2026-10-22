# traffic light: green 3 ticks, yellow 1, red 2
cars_through = 0
for tick in range(12):
    phase = tick % 6
    if phase < 3:
        print("green")
        cars_through += 2
    elif phase == 3:
        print("yellow")
        cars_through += 1
    else:
        print("red")
print(cars_through)
