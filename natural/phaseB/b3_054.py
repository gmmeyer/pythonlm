# smallest number divisible by every number from 1 to 4
n = 1
while True:
    ok = True
    for d in range(1, 5):
        if n % d != 0:
            ok = False
            break
    if ok:
        break
    n += 1
print(n)
