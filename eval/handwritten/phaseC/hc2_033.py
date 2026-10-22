t = 59
while t < 900:
    m = str(t // 60)
    s = str(t % 60)
    print("0" * (2 - len(m)) + m + ":" + "0" * (2 - len(s)) + s)
    t += 311
