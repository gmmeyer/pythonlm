for level in range(100, 0, -30):
    bars = level // 10
    line = "[" + "#" * bars + "-" * (10 - bars) + "] " + str(level) + "%"
    if level < 30:
        line += " LOW"
    print(line)
