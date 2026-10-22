n = 813
d0 = n % 7
n = n // 7
d1 = n % 7
n = n // 7
d2 = n % 7
n = n // 7
d3 = n % 7
n = n // 7
print(d3)
print(d2)
print(d1)
print(d0)
print(n)
back = ((d3 * 7 + d2) * 7 + d1) * 7 + d0
print(back)
