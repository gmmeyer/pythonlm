# Big X: two diagonals cross in the middle of a 9-row figure.
n = 9
mid = n // 2
r = 0
while r < n:
    if r < mid:
        line = " " * r + "\\" + " " * (n - 2 - 2 * r) + "/"
    elif r == mid:
        line = " " * r + "X"
    else:
        k = n - 1 - r
        line = " " * k + "/" + " " * (n - 2 - 2 * k) + "\\"
    print(line)
    r += 1
print("size:", n)
