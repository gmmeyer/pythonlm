# reverse the digits of 472, then check a palindrome
n = 472
rev = 0
while n > 0:
    rev = rev * 10 + n % 10
    n //= 10
print(rev)
m = 515
copy = m
back = 0
while copy > 0:
    back = back * 10 + copy % 10
    copy //= 10
print(back == m)
