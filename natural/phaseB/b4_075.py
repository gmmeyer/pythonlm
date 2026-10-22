# 1 - 2 + 3 - 4 + ... up to 20
total = 0
for i in range(1, 21):
    if i % 2 == 1:
        total += i
    else:
        total -= i
print(total)
