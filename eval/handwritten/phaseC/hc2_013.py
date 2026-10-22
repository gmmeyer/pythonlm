b = "1101101"
v = 0
for i in range(len(b)):
    v = v * 2
    if b[i] == "1":
        v += 1
w = 0
p = 1
i = len(b) - 1
while i >= 0:
    if b[i] == "1":
        w += p
    p *= 2
    i -= 1
print(b, v, w, v == w)
