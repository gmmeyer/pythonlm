# Checkerboard: a square is dark ('#') when row + column is even.
# Each row is followed by a count of its dark squares.
n = 5
r = 0
while r < n:
    line = ""
    dark = 0
    c = 0
    while c < n:
        if (r + c) % 2 == 0:
            line = line + "#"
            dark += 1
        else:
            line = line + "."
        c += 1
    print(line, end="  ")
    print("dark:", dark)
    r += 1
print("=" * n)
