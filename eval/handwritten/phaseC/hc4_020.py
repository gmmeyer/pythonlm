# Scoreboard: names left-aligned in 8 columns, scores right-aligned.
print("+--------+-----+")
print("| player | pts |")
print("+--------+-----+")
for k in range(5):
    if k == 0:
        name = "ada"
        pts = 120
    elif k == 1:
        name = "bob"
        pts = 95
    elif k == 2:
        name = "cyrus"
        pts = 310
    elif k == 3:
        name = "di"
        pts = 7
    else:
        name = "evelyn"
        pts = 64
    left = " " + name + " " * (7 - len(name))
    s = str(pts)
    right = " " * (4 - len(s)) + s + " "
    print("|" + left + "|" + right + "|")
print("+--------+-----+")
