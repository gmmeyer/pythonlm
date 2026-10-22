# trailing zeros of a few numbers, using a for loop to pick them
for n in range(8, 33, 8):
    z = 0
    m = n
    while m % 2 == 0:
        m //= 2
        z += 1
    print(z)
