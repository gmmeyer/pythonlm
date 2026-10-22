outer = 0
inner = 0
for i in range(3):
    outer += 1
    j = 0
    while True:
        j += 1
        inner += 1
        if j >= i + 2:
            break
print(outer)
print(inner)
print(j)
