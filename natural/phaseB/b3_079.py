# find the first multiple of 17 whose digits are all the same size apart
for n in range(17, 400, 17):
    h = n // 100
    t = n // 10 % 10
    u = n % 10
    if h > 0 and t - h == u - t:
        print(n)
        break
print(h)
print(t)
print(u)
