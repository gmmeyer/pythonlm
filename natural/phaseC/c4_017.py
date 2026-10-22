for pct in range(0, 101, 25):
    filled = pct // 10
    bar = "#" * filled + "." * (10 - filled)
    print(f"[{bar}] {pct}%")
