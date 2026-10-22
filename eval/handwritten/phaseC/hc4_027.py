# Stopwatch: five laps given in seconds, shown as MM:SS with splits.
split = 0
lap = 1
while lap <= 5:
    if lap == 1:
        secs = 75
    elif lap == 2:
        secs = 128
    elif lap == 3:
        secs = 59
    elif lap == 4:
        secs = 201
    else:
        secs = 97
    split += secs
    a = str(secs // 60)
    b = str(secs % 60)
    if len(b) == 1:
        b = "0" + b
    c = str(split // 60)
    d = str(split % 60)
    if len(d) == 1:
        d = "0" + d
    print(f"lap {lap}  {a}:{b}  split {c}:{d}")
    lap += 1
print("laps:", 5, "total seconds:", split)
