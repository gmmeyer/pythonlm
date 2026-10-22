pos = 0
moves = 0
path = ""
while pos < 6:
    if pos == 0 or pos == 2:
        pos += 1
        path = path + "E"
    elif pos == 1:
        pos += 2
        path = path + "S"
    else:
        pos += 1
        path = path + "N"
    moves += 1
print("Path:", path)
print("Moves:", moves)
