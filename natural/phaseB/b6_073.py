# hallway light stays on 5 ticks after the last motion
timer = 0
on_ticks = 0
for tick in range(30):
    if tick % 11 == 3 or tick % 13 == 0:
        timer = 5
    if timer > 0:
        on_ticks += 1
        timer -= 1
print(on_ticks)
print(timer)
