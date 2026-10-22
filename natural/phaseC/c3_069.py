n = 1
steps = 0
while len(str(n)) < 3:
    n = n * 2
    steps += 1
print("Reached", n, "after", steps, "doublings")
