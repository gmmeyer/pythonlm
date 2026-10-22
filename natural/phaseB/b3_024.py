total = 0
for i in range(1, 31, 2):
    if i == 15 or i == 21:
        continue
    total += i
print(total)
