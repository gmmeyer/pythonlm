pos = 0
neg = 0
zero = 0
for i in range(10):
    v = i * i - 25
    if v > 0:
        pos += 1
    elif v < 0:
        neg += 1
    else:
        zero += 1
print(pos)
print(neg)
print(zero)
