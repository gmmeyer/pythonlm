for t in range(-10, 40, 10):
    if t < 0:
        label = "freezing"
    elif t < 15:
        label = "cold"
    elif t < 25:
        label = "mild"
    else:
        label = "hot"
    print(f"{t} C is {label}")
