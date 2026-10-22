for n in range(-3, 4, 2):
    sign = "-" if n < 0 else "+"
    mag = -n if n < 0 else n
    print(sign + str(mag), str(n), sign + str(mag) == str(n))
