# kitchen timer in minutes and seconds
minutes = 2
seconds = 10
ticks = 0
while minutes > 0 or seconds > 0:
    if seconds == 0:
        minutes -= 1
        seconds = 50
    else:
        seconds -= 10
    ticks += 1
print(ticks)
print(minutes)
print(seconds)
