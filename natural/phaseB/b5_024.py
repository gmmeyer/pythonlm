# ways to climb n stairs for every n from 1 to 8
for n in range(1, 9):
    a = 1
    b = 1
    for s in range(n):
        a, b = b, a + b
    print(a)
