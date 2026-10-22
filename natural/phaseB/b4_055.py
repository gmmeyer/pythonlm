low = 100
high = -1
for i in range(1, 13):
    v = (i * i) % 17
    if v < low:
        low = v
    if v > high:
        high = v
print(low)
print(high)
