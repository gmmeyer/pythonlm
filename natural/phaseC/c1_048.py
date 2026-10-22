# hollow rectangle
w = 10
h = 5
print("#" * w)
for row in range(h - 2):
    print("#" + " " * (w - 2) + "#")
print("#" * w)
