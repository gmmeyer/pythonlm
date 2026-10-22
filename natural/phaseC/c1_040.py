minutes = 2
seconds = 3
for tick in range(6):
    s = str(seconds)
    if seconds < 10:
        s = "0" + s
    print(str(minutes) + ":" + s)
    if seconds == 0:
        minutes -= 1
        seconds = 59
    else:
        seconds -= 1
print("time check complete")
