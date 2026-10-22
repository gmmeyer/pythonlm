# multiplicative order of 2 modulo 11
x = 2
order = 1
while x != 1:
    x = x * 2 % 11
    order += 1
print(order)
