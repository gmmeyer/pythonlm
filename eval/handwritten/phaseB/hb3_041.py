last = -1
for i in range(1, 20):
    if i % 3 == 0:
        if i % 5 == 0:
            last = i
            break
        else:
            continue
    last = -i
print(last)
print(i)
