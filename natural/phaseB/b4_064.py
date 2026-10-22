n = 36
count = 0
d = 1
while d <= n:
    if n % d == 0:
        count += 1
    d += 1
print(count)
