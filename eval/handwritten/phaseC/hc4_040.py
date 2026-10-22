# A note card: lines are boxed and padded to the longest one.
# The lines are visited twice: once to measure, once to print.
l1 = "remember to"
l2 = "water the fern"
l3 = "feed the cat"
l4 = "and the fish"
w = 0
for k in range(4):
    if k == 0:
        t = l1
    elif k == 1:
        t = l2
    elif k == 2:
        t = l3
    else:
        t = l4
    if len(t) > w:
        w = len(t)
print(".-" + "-" * w + "-.")
for k in range(4):
    if k == 0:
        t = l1
    elif k == 1:
        t = l2
    elif k == 2:
        t = l3
    else:
        t = l4
    print("| " + t + " " * (w - len(t)) + " |")
print("'-" + "-" * w + "-'")
print("width", w, "lines", 4)
