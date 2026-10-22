s = "xo"
k = 1
while len(s) < 20:
    print(k, len(s), s)
    s = s * 2
    k += 1
print(len(s), s[-1], s[-len(s)])
s = s * -1
print("[" + s + "]", len(s))
