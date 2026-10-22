moves = "UURDDLLU"
x = 0
y = 0
for i in range(len(moves)):
    m = moves[i]
    if m == "U":
        y += 1
    elif m == "D":
        y -= 1
    elif m == "R":
        x += 1
    elif m == "L":
        x -= 1
print("final position:", x, y)
if x == 0 and y == 0:
    print("back at the start")
else:
    print("not back at the start")
