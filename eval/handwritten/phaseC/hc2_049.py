s = "abcd"
h = len(s)
for r in range(2 * h - 1):
    k = r
    if r >= h:
        k = 2 * h - 2 - r
    print(" " * (h - 1 - k) + s[k] * (2 * k + 1))
