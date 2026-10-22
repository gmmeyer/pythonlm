a = 0
b = 1
count = 0
while count < 15:
    a, b = b, a + b
    count += 1
print(a)
