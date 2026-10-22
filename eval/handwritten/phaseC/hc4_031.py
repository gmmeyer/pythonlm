# Concentric squares: each ring of a 9x9 figure uses the next
# character of a palette string, from the outside in.
pal = "#+:o."
n = 9
for r in range(n):
    dr = r
    if n - 1 - r < dr:
        dr = n - 1 - r
    left = ""
    right = ""
    for j in range(dr):
        left = left + pal[j]
        right = pal[j] + right
    print(left + pal[dr] * (n - 2 * dr) + right)
print("rings:", len(pal), "centre:", pal[-1])
