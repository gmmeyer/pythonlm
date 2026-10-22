# box around three lines
l1 = "Welcome"
l2 = "to the"
l3 = "library"
w = len(l1)
if len(l2) > w:
    w = len(l2)
if len(l3) > w:
    w = len(l3)
edge = "+" + "-" * (w + 2) + "+"
print(edge)
print("| " + l1 + " " * (w - len(l1)) + " |")
print("| " + l2 + " " * (w - len(l2)) + " |")
print("| " + l3 + " " * (w - len(l3)) + " |")
print(edge)
