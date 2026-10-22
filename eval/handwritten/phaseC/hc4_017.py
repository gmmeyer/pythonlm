# Progress bar from 0% to 100% in eight updates of a 16-cell bar.
total = 8
done = 0
while done <= total:
    filled = done * 2
    bar = "#" * filled + "." * (16 - filled)
    pct = done * 100 // total
    p = str(pct)
    while len(p) < 3:
        p = " " + p
    print(f"[{bar}] {p}%")
    done += 1
print("complete")
