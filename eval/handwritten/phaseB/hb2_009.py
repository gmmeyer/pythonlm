n = 9
for k in range(2, 5):
    j = 0
    for i in range(2, n + 1):
        j = (j + k) % i
    print(j + 1)
