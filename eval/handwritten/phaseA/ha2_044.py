w = 13
i = 97
r, c = i // w, i % w
print(r)
print(c)
print(r * w + (c - 1) % w)
print((r - 1) % 8 * w + c)
print((r + 3) % 8 * w + (c + 9) % w)
print((r * w + c - 200) % (8 * w))
