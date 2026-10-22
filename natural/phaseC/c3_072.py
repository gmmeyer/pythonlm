print("right aligned:")
for n in range(1, 400, 90):
    pad = " " * (5 - len(str(n)))
    print(pad + str(n) + "|")
