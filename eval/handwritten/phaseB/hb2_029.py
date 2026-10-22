a = 7
b = 9
c = 12
x = 0
p = 1
u = a
v = b
w = c
while u + v + w > 0:
    if (u % 2 + v % 2 + w % 2) % 2 == 1:
        x += p
    u //= 2
    v //= 2
    w //= 2
    p *= 2
print(x)
h = 1
while h * 2 <= x:
    h *= 2
if x == 0:
    print('lose')
elif a // h % 2 == 1:
    print('a')
elif b // h % 2 == 1:
    print('b')
else:
    print('c')
