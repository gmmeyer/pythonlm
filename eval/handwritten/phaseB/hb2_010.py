j = 0
p = 1
ok = True
for n in range(2, 20):
    j = (j + 2) % n
    if p * 2 <= n:
        p *= 2
    if j + 1 != 2 * (n - p) + 1:
        ok = False
        break
print(ok)
print(j + 1)
