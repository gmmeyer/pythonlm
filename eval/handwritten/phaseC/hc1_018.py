level = 73
while level > 0:
    filled = level // 10
    gauge = "[" + "|" * filled + "." * (10 - filled) + "]"
    print("battery", gauge, str(level) + "%")
    if level < 30:
        print("plug in soon")
    level -= 25
print("screen off")
