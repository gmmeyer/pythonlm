# traffic light state machine
state = 0
for tick in range(10):
    if state == 0:
        print("Green")
        if tick % 3 == 2:
            state = 1
    elif state == 1:
        print("Yellow")
        state = 2
    else:
        print("Red")
        state = 0
