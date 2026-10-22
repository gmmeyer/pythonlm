# Traffic light state machine: green 4 ticks, yellow 1, red 3.
# Each tick prints the lamp column with the active lamp lit.
state = "green"
left = 4
for tick in range(12):
    r = "( )"
    y = "( )"
    g = "( )"
    if state == "red":
        r = "(R)"
    elif state == "yellow":
        y = "(Y)"
    else:
        g = "(G)"
    print(tick, r + y + g, state, sep="  ")
    left -= 1
    if left == 0:
        if state == "green":
            state = "yellow"
            left = 1
        elif state == "yellow":
            state = "red"
            left = 3
        else:
            state = "green"
            left = 4
print("cycle length", 4 + 1 + 3)
