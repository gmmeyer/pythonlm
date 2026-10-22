first = True
for n in range(7, 60, 7):
    if not first:
        print(end=", ")
    print(n, end="")
    first = False
print()
