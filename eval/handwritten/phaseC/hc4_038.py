# Bordered table of n, n squared and n cubed for n = 1..8.
# Each column is right-aligned by measuring its string with len().
print("+----+-----+-----+")
print("|  n |  sq | cube|")
print("+----+-----+-----+")
n = 1
while n <= 8:
    a = str(n)
    b = str(n * n)
    c = str(n * n * n)
    row = "| " + " " * (2 - len(a)) + a
    row = row + " | " + " " * (3 - len(b)) + b
    row = row + " | " + " " * (3 - len(c)) + c + " |"
    print(row)
    n += 1
print("+----+-----+-----+")
