s = 0
for i in range(6):
    if i % 2 == 0:
        s += i
    else:
        s -= 1
    continue
print(s)
n = 0
while n < 5:
    n += 1
    if n == 3:
        print(n)
    continue
print(n)
