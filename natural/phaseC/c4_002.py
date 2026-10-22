total = 5
for i in range(1, total + 1):
    print("Step", i, "of", total, end=": ")
    if i % 2 == 0:
        print("skipped")
    else:
        print("done")
