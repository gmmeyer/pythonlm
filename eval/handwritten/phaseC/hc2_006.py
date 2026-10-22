w = 4
n = 7
while n < 300:
    t = str(n)
    print("0" * (w - len(t)) + t, end=" ")
    n = n * 3 + 1
print("|")
