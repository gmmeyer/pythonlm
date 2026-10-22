count = 0
for n in range(1, 101):
    if n % 3 == 0 and not n % 5 == 0:
        count += 1
print(count)
