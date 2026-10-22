count = 0
for i in range(4):
    for j in range(4):
        if j > i:
            break
        count += 1
    print(count)
print(i)
print(j)
