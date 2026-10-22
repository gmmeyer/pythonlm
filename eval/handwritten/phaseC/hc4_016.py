# Hourglass: rows shrink to a single grain, then widen again.
# Sand ('.') fills the bottom half, the top half is drawn with ':'.
top = 9
print("+" + "-" * top + "+")
w = top
pad = 0
while w >= 1:
    print(" " * pad + "\\" + ":" * w + "/")
    w -= 2
    pad += 1
w = 1
pad -= 1
while w <= top:
    print(" " * pad + "/" + "." * w + "\\")
    w += 2
    pad -= 1
print("+" + "-" * top + "+")
