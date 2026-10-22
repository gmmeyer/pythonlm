for n in range(5, 10):
    b = ""
    m = n
    while m > 0:
        b = str(m % 2) + b
        m //= 2
    pad = "0" * (6 - len(b))
    print(f"{n} {pad + b} {len(b)}")
