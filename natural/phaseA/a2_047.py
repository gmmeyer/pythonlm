# convert 137 to base 5
n = 137
d0 = n % 5
n //= 5
d1 = n % 5
n //= 5
d2 = n % 5
n //= 5
d3 = n % 5
print(d3)
print(d2)
print(d1)
print(d0)
