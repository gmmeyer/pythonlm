for mins in range(59, 182, 61):
    h = mins // 60
    m = mins % 60
    out = ""
    if h > 0:
        out = str(h) + " hour"
        if h != 1:
            out += "s"
        out += ", "
    out += str(m) + " minute"
    if m != 1:
        out += "s"
    print(mins, "->", out)
