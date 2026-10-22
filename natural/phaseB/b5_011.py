n = 96
while n > 1 and n % 2 == 0:
    n //= 2
if n == 1:
    print("power of two")
else:
    print("not a power of two")
print(n)
