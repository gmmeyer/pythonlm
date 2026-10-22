state = 0
steps = 0
while state != 9:
    steps += 1
    if state == 0:
        print("You wake up in a dark cave.")
        state = 1
    elif state == 1:
        print("You see a light to the north.")
        state = 2
    elif state == 2:
        print("A bridge crosses a river.")
        state = 3
    elif state == 3:
        print("You cross the bridge safely.")
        state = 9
print("You escaped in", steps, "steps!")
