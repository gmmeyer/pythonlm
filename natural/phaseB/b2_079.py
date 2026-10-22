# traffic light countdown printing the color changes only
state = 0
for sec in range(0, 40, 5):
    new_state = (sec // 10) % 3
    if new_state != state:
        state = new_state
        if state == 0:
            print("green")
        elif state == 1:
            print("yellow")
        else:
            print("red")
print(state)
