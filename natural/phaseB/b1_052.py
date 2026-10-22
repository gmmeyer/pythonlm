total = 0
for i in range(1, 16):
    if i % 2 == 0:
        continue
    total += i * i
print(total)
