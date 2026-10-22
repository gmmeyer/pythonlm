# Multiplication table for 1..5 with a header row and separators.
# Each cell is right-aligned to width 4 by padding with spaces.
n = 5
header = "   |"
for c in range(1, n + 1):
    s = str(c)
    header = header + " " * (4 - len(s)) + s
print(header)
print("---+" + "-" * (4 * n))
for r in range(1, n + 1):
    line = " " + str(r) + " |"
    for c in range(1, n + 1):
        s = str(r * c)
        line = line + " " * (4 - len(s)) + s
    print(line)
print("---+" + "-" * (4 * n))
