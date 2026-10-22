a = 17
m = 43
r0 = m
r1 = a
t0 = 0
t1 = 1
while r1 != 0:
    q = r0 // r1
    r0, r1 = r1, r0 - q * r1
    t0, t1 = t1, t0 - q * t1
if t0 < 0:
    t0 += m
print(r0)
print(t0)
print(a * t0 % m == 1)
