fails = 0
for attempt in range(1, 8):
    if attempt % 3 != 0:
        fails += 1
        print(f"[{attempt}] login failed for admin ({fails} in a row)")
    else:
        fails = 0
        print(f"[{attempt}] login ok")
    if fails >= 2 and attempt > 5:
        print(f"[{attempt}] ALERT too many failures")
        break
