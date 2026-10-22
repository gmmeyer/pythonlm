# A week of temperatures, some below zero, plotted around a zero line.
# Each mark sits at column (temp + 6); '|' marks zero degrees.
lo = 999
hi = -999
for day in range(7):
    if day == 0:
        t = -4
    elif day == 1:
        t = -1
    elif day == 2:
        t = 3
    elif day == 3:
        t = 8
    elif day == 4:
        t = 12
    elif day == 5:
        t = 5
    else:
        t = -2
    if t < lo:
        lo = t
    if t > hi:
        hi = t
    if t < 0:
        line = " " * (6 + t) + "*" + " " * (-t - 1) + "|"
    elif t == 0:
        line = " " * 6 + "*"
    else:
        line = " " * 6 + "|" + " " * (t - 1) + "*"
    print("day", day + 1, line, t)
print("low", lo, "high", hi, "range", hi - lo)
