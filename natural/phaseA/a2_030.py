# how far is a number from its mirror image?
n = 342
a = n // 100
b = n // 10 % 10
c = n % 10
rev = c * 100 + b * 10 + a
print(rev)
print(n - rev)
