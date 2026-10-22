sym = "IVXLCDM"
n = 649
m = n
out = ""
p = 0
while m > 0:
    d = m % 10
    one = sym[p]
    if d == 9:
        part = one + sym[p + 2]
    elif d >= 5:
        part = sym[p + 1] + one * (d - 5)
    elif d == 4:
        part = one + sym[p + 1]
    else:
        part = one * d
    out = part + out
    m //= 10
    p += 2
print(n, out)
