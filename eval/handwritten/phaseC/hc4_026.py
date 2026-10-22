# Six-bit binary for a handful of numbers, built from the low bit up.
for k in range(5):
    if k == 0:
        n = 5
    elif k == 1:
        n = 18
    elif k == 2:
        n = 37
    elif k == 3:
        n = 63
    else:
        n = 44
    bits = ""
    m = n
    ones = 0
    for b in range(6):
        if m % 2 == 1:
            bits = "1" + bits
            ones += 1
        else:
            bits = "0" + bits
        m //= 2
    s = str(n)
    if len(s) < 2:
        s = " " + s
    print(s, "=", bits, "ones:", ones)
