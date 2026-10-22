# digital root of 789
n = 789
s = n // 100 + n // 10 % 10 + n % 10
print(s)
root = s // 10 + s % 10
print(root)
