# longest run of heads in 30 flips of a seeded generator
x = 11
run = 0
best = 0
for flip in range(30):
    x = (x * 13 + 7) % 64
    if x >= 32:
        run += 1
        if run > best:
            best = run
    else:
        run = 0
print(best)
