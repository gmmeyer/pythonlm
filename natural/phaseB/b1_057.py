# Harshad numbers from 100 to 124
for n in range(100, 125):
    s = n // 100 + n // 10 % 10 + n % 10
    if n % s == 0:
        print(n)
