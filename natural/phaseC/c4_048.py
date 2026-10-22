pages = 4
for p in range(1, pages + 1):
    if p > 1:
        left = "<"
    else:
        left = " "
    if p < pages:
        right = ">"
    else:
        right = " "
    print(left, "Page", p, "of", pages, right)
