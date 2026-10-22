n = 123
rev = 0
for i in range(3):
    rev = rev * 10 + n % 10
    n //= 10
print(rev)
