# biggest jump between neighbouring squares mod 17
prev = 0
big = 0
where = 0
for i in range(1, 17):
    cur = i * i % 17
    d = cur - prev
    if d < 0:
        d = -d
    if d > big:
        big = d
        where = i
    prev = cur
print(big)
print(where)
