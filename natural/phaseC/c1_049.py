n = 5
for r in range(n):
    line = ""
    for c in range(n):
        if r == c or r + c == n - 1:
            line = line + "X"
        else:
            line = line + "."
    print(line)
