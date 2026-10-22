floor = 0
for step in range(5):
    if step == 0:
        move = 3
    elif step == 1:
        move = -4
    elif step == 2:
        move = 1
    elif step == 3:
        move = 6
    else:
        move = -2
    floor += move
    if floor == 0:
        label = "G"
    elif floor < 0:
        label = "B" + str(-floor)
    else:
        label = str(floor)
    if move > 0:
        arrow = "up"
    else:
        arrow = "down"
    print("going " + arrow + " to " + label)
print("doors open")
