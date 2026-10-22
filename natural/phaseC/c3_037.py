print("C", "F", sep="\t")
for c in range(0, 41, 10):
    f = c * 9 // 5 + 32
    print(c, f, sep="\t")
