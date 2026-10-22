# sum of 1..44, skipping anything divisible by 10
total = 0
for n in range(1, 45):
    if n % 10 == 0:
        continue
    total += n
print(total)
