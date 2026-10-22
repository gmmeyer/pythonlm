print("n", "binary", sep=" | ")
for n in range(5, 40, 7):
    bits = ""
    x = n
    while x > 0:
        bits = str(x % 2) + bits
        x = x // 2
    print(n, bits, sep=" | ")
