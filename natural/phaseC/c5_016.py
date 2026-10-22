bits = "1101110011111"
best = 0
run = 0
for i in range(len(bits)):
    if bits[i] == "1":
        run += 1
        if run > best:
            best = run
    else:
        run = 0
print("longest streak of ones:", best)
