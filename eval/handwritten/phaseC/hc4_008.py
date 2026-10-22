# A clock starting at 21:50 that ticks forward 47 minutes at a time.
# Each field is zero-padded by checking the length of its string.
h = 21
m = 50
for tick in range(9):
    hs = str(h)
    if len(hs) < 2:
        hs = "0" + hs
    ms = str(m)
    if len(ms) < 2:
        ms = "0" + ms
    print(f"tick {tick}: {hs}:{ms}")
    m += 47
    while m >= 60:
        m -= 60
        h += 1
    if h >= 24:
        h -= 24
        print("-- midnight --")
