# is 145 equal to the sum of the factorials of its digits?
n = 145
m = n
total = 0
while m > 0:
    d = m % 10
    f = 1
    for k in range(2, d + 1):
        f *= k
    total += f
    m //= 10
print(total == n)
