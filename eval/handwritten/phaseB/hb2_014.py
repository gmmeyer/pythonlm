for i in range(2, 10):
    if i % 2 == 0:
        continue
    for j in range(2, 11):
        if i * j % 11 == 1:
            print(j)
            break
