for n in range(0, 27, 4):
    t = ""
    m = n
    while m > 0:
        t = str(m % 3) + t
        m //= 3
    t = "0" * (3 - len(t)) + t
    print(t, end=" ")
print("<- base 3")
