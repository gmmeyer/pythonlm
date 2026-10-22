num = 438
p = num // 100
p *= num // 10 % 10
p *= num % 10
print("digit product:")
print(p)
