n = 28
total = 0
for d in range(1, n):
    if n % d == 0:
        total += d
if total == n:
    print("perfect")
else:
    print("not perfect")
