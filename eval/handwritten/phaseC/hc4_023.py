# Centre several titles inside a fixed-width frame.
# Left padding is (width - len) // 2, the rest goes on the right.
width = 24
print("*" * (width + 2))
for k in range(4):
    if k == 0:
        title = "GRAND MENU"
    elif k == 1:
        title = "soup"
    elif k == 2:
        title = "roast and greens"
    else:
        title = "pie"
    left = (width - len(title)) // 2
    right = width - len(title) - left
    print("*" + " " * left + title + " " * right + "*")
    if k == 0:
        print("*" + "~" * width + "*")
print("*" * (width + 2))
