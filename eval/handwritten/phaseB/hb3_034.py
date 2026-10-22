s = 0
for i in range(4):
    for j in range(i, 2):
        s += 10
    for j in range(2, i):
        if j == 2:
            s += 1
        else:
            break
print(s)
print(i)
print(j)
