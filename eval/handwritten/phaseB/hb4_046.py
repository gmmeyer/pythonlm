# A microwave as a state machine: 0 = running, 1 = paused (door open),
# 2 = paused (door shut, waiting for start), 3 = done. Each tick is 5
# seconds off a 45 second timer. The door opens on ticks 3 and 9, shuts two
# ticks later, and start is pressed one tick after that.
state = 0
left = 45
tick = 0
pauses = 0
print("microwave")
while state != 3:
    tick += 1
    if state == 0:
        if tick == 3 or tick == 9:
            state = 1
            pauses += 1
            print("door opened")
        else:
            left -= 5
            if left == 0:
                state = 3
                print("beep")
    elif state == 1:
        if tick == 5 or tick == 11:
            state = 2
            print("door shut")
    else:
        if tick == 6 or tick == 12:
            state = 0
            print("start pressed")
    print(left)
print("ticks and pauses")
print(tick)
print(pauses)
