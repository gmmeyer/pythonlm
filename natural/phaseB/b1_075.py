count = 0
for n in range(1, 41):
    if n % 3 == 0 and not n % 2 == 0:
        count += 1
print(count)
