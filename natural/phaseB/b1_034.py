# perimeters of primitive Pythagorean triples from Euclid's formula
for m in range(2, 6):
    for n in range(1, m):
        if (m - n) % 2 == 1:
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            print(a + b + c)
