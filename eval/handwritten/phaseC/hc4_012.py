# Hollow triangle: only the two slanted sides and the base are drawn.
n = 7
r = 1
while r <= n:
    pad = " " * (n - r)
    if r == 1:
        body = "^"
    elif r == n:
        body = "=" * (2 * n - 1)
    else:
        body = "/" + " " * (2 * r - 3) + "\\"
    print(pad + body, end="")
    print("  <-", 2 * r - 1)
    r += 1
print("height", n, sep="=")
