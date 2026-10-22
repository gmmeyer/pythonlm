print("F    C")
f = 32
while f <= 212:
    c = (f - 32) * 5 // 9
    print(f, " " * (4 - len(str(f))), c, sep="")
    f += 45
