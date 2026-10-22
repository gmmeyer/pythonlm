# Pythagorean triples from Euclid's formula, hypotenuse at most 40
for m in range(2, 7):
    for n in range(1, m):
        c = m * m + n * n
        if c <= 40 and (m - n) % 2 == 1:
            print(m * m - n * n)
            print(2 * m * n)
            print(c)
            print()
