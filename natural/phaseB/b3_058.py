# sum of the numbers from 50 down to 1 that end in 3
total = 0
for n in range(50, 0, -1):
    if n % 10 != 3:
        continue
    total += n
print(total)
