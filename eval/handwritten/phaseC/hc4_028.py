# Elevator log: it serves a fixed queue of floor requests,
# printing one line per floor it passes.
floor = 1
for req in range(4):
    if req == 0:
        goal = 5
    elif req == 1:
        goal = 2
    elif req == 2:
        goal = 7
    else:
        goal = 4
    print("call to floor", goal)
    while floor != goal:
        if floor < goal:
            floor += 1
            arrow = "^"
        else:
            floor -= 1
            arrow = "v"
        print("  " + arrow + " " + str(floor) + " " + "=" * floor)
    print("  doors open at", floor)
