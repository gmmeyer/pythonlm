# Diamond of stars with a '+' marking the centre column.
# The top half grows by two stars per row, the bottom half shrinks.
size = 6
i = 1
while i <= size:
    side = "*" * (i - 1)
    print(" " * (size - i) + side + "+" + side, end="")
    print("   row", i)
    i += 1
i = size - 1
while i >= 1:
    side = "*" * (i - 1)
    print(" " * (size - i) + side + "+" + side, end="")
    print("   row", 2 * size - i)
    i -= 1
width = 2 * size - 1
print("widest row:", width, "chars")
print("total rows:", 2 * size - 1, sep=" ")
