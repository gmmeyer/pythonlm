# smallest factor of 221
n = 221
d = 2
while d < n and n % d != 0:
    d += 1
print(d)
