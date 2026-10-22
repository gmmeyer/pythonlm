# times table with a header row
print("*", end="\t")
for c in range(1, 7):
    print(c, end="\t")
print()
for r in range(1, 7):
    print(r, end="\t")
    for c in range(1, 7):
        print(r * c, end="\t")
    print()
