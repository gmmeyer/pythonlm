# stopwatch laps
total = 0
for lap in range(1, 5):
    total += 47 + lap * 9
    m = total // 60
    s = total % 60
    pad = ""
    if s < 10:
        pad = "0"
    print(f"lap {lap}: {m}:{pad}{s}")
