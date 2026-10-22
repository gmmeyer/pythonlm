# Fermat's little theorem for p = 13
p = 13
for a in range(2, 6):
    r = 1
    for i in range(p - 1):
        r = r * a % p
    print(r)
