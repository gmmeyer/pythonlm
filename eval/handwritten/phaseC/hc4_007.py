# Histogram of the last digit of the squares 1*1 .. 20*20.
# Only six digits can ever end a square; each gets a bar of '#'.
c0 = c1 = c4 = c5 = c6 = c9 = 0
k = 1
while k <= 20:
    d = k * k % 10
    if d == 0:
        c0 += 1
    elif d == 1:
        c1 += 1
    elif d == 4:
        c4 += 1
    elif d == 5:
        c5 += 1
    elif d == 6:
        c6 += 1
    else:
        c9 += 1
    k += 1
print("last digit of k*k, k = 1..20")
print("0 |" + "#" * c0, c0)
print("1 |" + "#" * c1, c1)
print("4 |" + "#" * c4, c4)
print("5 |" + "#" * c5, c5)
print("6 |" + "#" * c6, c6)
print("9 |" + "#" * c9, c9)
print("never: 2 3 7 8")
