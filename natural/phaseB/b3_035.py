# row sums of a 5x5 multiplication table
for i in range(1, 6):
    row = 0
    for j in range(1, 6):
        row += i * j
    print(row)
