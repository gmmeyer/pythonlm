total = 7
for done in range(total + 1):
    w = done * 20 // total
    bar = "#" * w + "-" * (20 - w)
    print("[" + bar + "]", str(done * 100 // total) + "%")
