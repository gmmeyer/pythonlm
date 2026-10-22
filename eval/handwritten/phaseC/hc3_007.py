x = "ab" * 2
y = "a" + "ba" + "b"
z = "abba"
print(x, y, z)
print(x == y, x == z, y != z, x != y)
w = ""
i = 0
while i < 4:
    if i % 2 == 0:
        w += "a"
    else:
        w += "b"
    i += 1
print(f"{w} {w == x} {w + z} {len(w + z)}")
