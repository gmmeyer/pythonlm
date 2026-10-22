# 6x6 multiplication table
for r in range(1, 7):
    for c in range(1, 7):
        p = r * c
        if p < 10:
            print(" ", end="")
        print(p, end=" ")
    print()
