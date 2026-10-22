t = 0
for n in range(20, 28):
    k = n
    c = 0
    while k:
        c += k % 2
        k //= 2
    if c == 3:
        print(n)
    t += c
print(t)
