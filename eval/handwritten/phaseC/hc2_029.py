b = "1011010"
g = b[0]
for i in range(1, len(b)):
    if b[i] == b[i - 1]:
        g += "0"
    else:
        g += "1"
back = g[0]
for i in range(1, len(g)):
    if g[i] == back[-1]:
        back += "0"
    else:
        back += "1"
print("bin", b, "gray", g, "back", back, back == b)
