# accumulate odd numbers, skipping multiples of 5, until -1 sentinel
n = 1
acc = 0
while n != -1:
    if n % 5 == 0:
        n += 2
        continue
    acc += n
    n += 2
    if acc > 60:
        n = -1
print(acc)
