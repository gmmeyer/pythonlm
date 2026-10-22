count = 0
for n in range(10, 60):
    if n // 10 + n % 10 == 9:
        count += 1
print(count)
