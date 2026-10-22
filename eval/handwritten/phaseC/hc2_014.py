H = "0123456789abcdef"
n = 750
base = 16
while base >= 2:
    m = n
    d = ""
    while m > 0:
        d = H[m % base] + d
        m //= base
    print(f"{n} in base {base}: {d}")
    base //= 2
