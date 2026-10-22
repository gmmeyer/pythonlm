# Right-aligned triangle of stars, then the same triangle upside down.
# Each row is built from repeated spaces and stars.
height = 6
row = 1
while row <= height:
    pad = " " * (height - row)
    stars = "*" * row
    print(pad + stars)
    row += 1
print("-" * (height + 2))
for r in range(height, 0, -1):
    line = ""
    for c in range(r):
        line = line + "*"
    print(" " * (height - r) + line, end="|\n")
print("rows:", height * 2, sep=" ")
