# traffic light cycle: 0 green, 1 yellow, 2 red
light = 0
green_time = 0
for tick in range(30):
    if light == 0 and tick % 5 == 4:
        light = 1
    elif light == 1:
        light = 2
    elif light == 2 and tick % 3 == 0:
        light = 0
    if light == 0:
        green_time += 1
print(light)
print(green_time)
