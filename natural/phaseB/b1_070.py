# reverse-and-add until a palindrome appears
n = 57
steps = 0
while steps < 5:
    m = n
    rev = 0
    while m > 0:
        rev = rev * 10 + m % 10
        m //= 10
    if rev == n:
        break
    n += rev
    steps += 1
print(n)
print(steps)
