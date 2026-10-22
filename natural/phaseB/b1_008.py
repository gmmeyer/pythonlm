n = 454
m = n
rev = 0
while m > 0:
    rev = rev * 10 + m % 10
    m //= 10
if rev == n:
    print("palindrome")
else:
    print("not a palindrome")
