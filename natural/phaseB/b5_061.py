# digital root of 987 by repeated digit sums
n = 987
rounds = 0
while n >= 10:
    s = 0
    while n > 0:
        s += n % 10
        n //= 10
    n = s
    rounds += 1
print(n)
print(rounds)
