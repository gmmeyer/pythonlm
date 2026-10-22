n = 987
if n == 0:
    root = 0
elif n % 9 == 0:
    root = 9
else:
    root = n % 9
print(root)
