n = 105
L = 2
w = 0
while L * (L + 1) // 2 <= n:
    r = n - L * (L - 1) // 2
    if r % L == 0:
        print(r // L)
        w += 1
    L += 1
print(w)
