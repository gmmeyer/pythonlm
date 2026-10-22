n = 613
b = ""
k = 0
while n > 0 or k % 4 != 0:
    if k > 0 and k % 4 == 0:
        b = " " + b
    b = str(n % 2) + b
    n //= 2
    k += 1
print(b)
