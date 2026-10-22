# fake class results from a scrambled seed
seed = 17
a = 0
b = 0
c = 0
f = 0
for i in range(12):
    seed = (seed * 7 + 13) % 100
    if seed >= 80:
        a += 1
    elif seed >= 60:
        b += 1
    elif seed >= 40:
        c += 1
    else:
        f += 1
print("A:", a, "B:", b, "C:", c, "F:", f)
