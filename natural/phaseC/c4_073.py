temp = 17
mode = "idle"
for step in range(8):
    if temp < 18:
        mode = "heating"
    elif temp > 22:
        mode = "cooling"
    else:
        mode = "idle"
    print(f"temp {temp}: {mode}")
    if mode == "heating":
        temp += 2
    elif mode == "cooling":
        temp -= 2
    else:
        temp += 3
