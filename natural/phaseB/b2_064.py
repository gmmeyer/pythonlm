# elevator door state machine: 0 closed, 1 opening, 2 open, 3 closing
door = 0
open_ticks = 0
for tick in range(16):
    if door == 0:
        if tick % 5 == 0:
            door = 1
    elif door == 1:
        door = 2
    elif door == 2:
        open_ticks += 1
        if open_ticks % 2 == 0:
            door = 3
    else:
        door = 0
print(door)
print(open_ticks)
