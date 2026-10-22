# binary digits of 37, lowest bit first
n = 37
while n > 0:
    print(n % 2)
    n //= 2
