# Hollow diamond: two stars per row except the top and bottom points.
n = 6
r = 0
while r < 2 * n - 1:
    if r < n:
        k = r
    else:
        k = 2 * n - 2 - r
    if k == 0:
        line = " " * (n - 1) + "*"
    else:
        line = " " * (n - 1 - k) + "*" + " " * (2 * k - 1) + "*"
    print(line)
    r += 1
print("rows:", 2 * n - 1)
