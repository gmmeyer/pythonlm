# smallest n with n! above 500
n = 1
f = 1
while f <= 500:
    n += 1
    f *= n
print(n)
print(f)
