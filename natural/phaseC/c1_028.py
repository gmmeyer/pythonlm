total = 8
for done in range(0, total + 1, 2):
    pct = done * 100 // total
    bar = "#" * done + "-" * (total - done)
    print(f"[{bar}] {pct}%")
