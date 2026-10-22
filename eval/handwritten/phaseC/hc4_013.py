# A staircase climbing to the right, with the height of each step.
steps = 7
level = 0
for s in range(steps):
    tread = "  " * s + "|__"
    level += 3
    print(tread + " " * (2 * (steps - s)) + "h=" + str(level))
print("=" * (2 * steps + 9))
# now walk back down, one step per line
for s in range(steps - 1, -1, -1):
    print("  " * s + "__|", end="")
    print(" down to", level - 3)
    level -= 3
