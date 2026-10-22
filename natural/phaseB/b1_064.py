# prime factors of 252, with repeats
n = 252
f = 2
while n > 1:
    if n % f == 0:
        print(f)
        n //= f
    else:
        f += 1
