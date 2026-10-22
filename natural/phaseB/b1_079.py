# Wilson's theorem for p = 7
p = 7
f = 1
for k in range(2, p):
    f = f * k % p
print(f)
print(f == p - 1)
