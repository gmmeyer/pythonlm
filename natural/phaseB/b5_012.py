# how many powers of two are there up to 32?
count = 0
for n in range(1, 33):
    m = n
    while m % 2 == 0:
        m = m // 2
    if m == 1:
        count += 1
print(count)
