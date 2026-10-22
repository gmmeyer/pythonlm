# Countdown timer from 01:02:05, stepping down 13 min 47 s at a time.
# Hours, minutes and seconds are kept separately and borrow by hand.
h = 1
m = 2
s = 5
while h > 0 or m > 0 or s > 0:
    hs = str(h)
    ms = str(m)
    ss = str(s)
    if len(hs) < 2:
        hs = "0" + hs
    if len(ms) < 2:
        ms = "0" + ms
    if len(ss) < 2:
        ss = "0" + ss
    print(hs + ":" + ms + ":" + ss)
    s -= 47
    if s < 0:
        s += 60
        m -= 1
    m -= 13
    if m < 0:
        m += 60
        h -= 1
    if h < 0:
        h = 0
        m = 0
        s = 0
print("00:00:00 ring!")
