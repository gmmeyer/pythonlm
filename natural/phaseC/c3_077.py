color = "red"
for step in range(5):
    if color == "red":
        color = "green"
    elif color == "green":
        color = "yellow"
    else:
        color = "red"
    print(step, color)
