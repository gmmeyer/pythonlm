print("loading", end="")
steps = 0
while steps < 6:
    print(".", end="")
    steps += 1
print(" done")
bar = ""
for k in range(4):
    bar += "=="
    print("[" + bar + ">" + " " * (8 - len(bar)) + "]")
print("installed", len(bar) // 2, "parts")
