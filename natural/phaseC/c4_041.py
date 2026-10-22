# requests per day, drawn as bars
for d in range(1, 6):
    n = (d * 7) % 6 + 1
    print("day", d, "#" * n, n)
