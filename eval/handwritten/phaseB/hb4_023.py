# Tug of war. The marker starts at 0; negative means Left is winning.
# Left starts strong (9) but tires by one every other tick, down to 3.
# Right pulls a steady 8 but slips to 2 on every fourth tick.
# Dragging the marker 15 units your way wins. The marker is shown every
# third tick.
marker = 0
left = 9
right = 8
tick = 0
print("tug of war")
while -15 < marker < 15 and tick < 24:
    tick += 1
    pull_right = right
    if tick % 4 == 0:
        pull_right = 2
    marker += pull_right - left
    if tick % 2 == 0 and left > 3:
        left -= 1
    if tick % 3 == 0:
        print(marker)
if marker >= 15:
    print("right wins")
elif marker <= -15:
    print("left wins")
else:
    print("time is up")
print(tick)
