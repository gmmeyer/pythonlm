# The tide rises and falls between 2 and 14 in steps of 2. Boats need a
# depth of at least 8 to enter the harbour. A boat arrives every third
# tick; waiting boats enter when the tide allows, at most 2 per tick.
tide = 2
direction = 2
waiting = 0
docked = 0
print("harbour")
for tick in range(20):
    tide += direction
    if tide == 14 or tide == 2:
        direction = -direction
    if tick % 3 == 0:
        waiting += 1
    if tide >= 8:
        enter = waiting
        if enter > 2:
            enter = 2
        waiting -= enter
        docked += enter
    if tick % 4 == 3:
        print(tide)
        print(waiting)
print("docked")
print(docked)
print(waiting)
