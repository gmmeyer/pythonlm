# deterministic pseudo-random sequence
x = 5
for i in range(10):
    x = (x * 7 + 3) % 101
    print(x)
