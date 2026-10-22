# find a pair with product 36 and sum 13
found = False
for a in range(1, 10):
    for b in range(a, 10):
        if a * b == 36 and a + b == 13:
            print(a)
            print(b)
            found = True
            break
    if found:
        break
