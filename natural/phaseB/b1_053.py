# 50 as a sum of two squares
n = 50
for a in range(1, 8):
    for b in range(a, 8):
        if a * a + b * b == n:
            print(a)
            print(b)
