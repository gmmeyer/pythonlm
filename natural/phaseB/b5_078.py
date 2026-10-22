# sort three numbers with compare and swap, then print them
a = 41
b = 7
c = 19
if a > b:
    a, b = b, a
if b > c:
    b, c = c, b
if a > b:
    a, b = b, a
print(a)
print(b)
print(c)
