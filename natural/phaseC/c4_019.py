light = "green"
timer = 0
for tick in range(12):
    print(tick, light)
    timer += 1
    if light == "green" and timer == 4:
        light = "yellow"
        timer = 0
    elif light == "yellow" and timer == 1:
        light = "red"
        timer = 0
    elif light == "red" and timer == 3:
        light = "green"
        timer = 0
