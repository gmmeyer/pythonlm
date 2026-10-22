shape = "^"
rows = 5
for i in range(1, rows + 1):
    print(" " * (rows - i) + shape * (2 * i - 1))
