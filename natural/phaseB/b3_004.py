# how many two-digit numbers have digits that add up to 10?
count = 0
for n in range(10, 100):
    if n // 10 + n % 10 == 10:
        count += 1
print(count)
