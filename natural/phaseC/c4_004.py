door = "closed"
for n in range(10):
    r = n % 4
    if r == 0 and door == "closed":
        door = "open"
    elif r == 1 and door == "open":
        door = "closed"
    elif r == 2 and door == "closed":
        door = "locked"
    elif r == 3 and door == "locked":
        door = "closed"
    print("tick", n, "door is", door)
