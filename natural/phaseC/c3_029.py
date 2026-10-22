for d in range(1, 8):
    if d == 1:
        day = "Mon"
    elif d == 2:
        day = "Tue"
    elif d == 3:
        day = "Wed"
    elif d == 4:
        day = "Thu"
    elif d == 5:
        day = "Fri"
    elif d == 6:
        day = "Sat"
    else:
        day = "Sun"
    if d >= 6:
        kind = "weekend"
    else:
        kind = "weekday"
    print(day, kind)
