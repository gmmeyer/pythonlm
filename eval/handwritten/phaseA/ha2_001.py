x = 739
s = x % 10 + x // 10 % 10 + x // 100
print(s)
print(x % 9)
print(s % 9)
print((x - s) // 9)
