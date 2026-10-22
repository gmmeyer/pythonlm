# digital root of 789
n = 789
while n > 9:
    s = 0
    while n > 0:
        s += n % 10
        n //= 10
    n = s
print(n)
