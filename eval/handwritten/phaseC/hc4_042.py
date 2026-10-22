# Game log: points scored each round from a simple formula, with a
# running total drawn as a bar of '+' (one per 10 points).
total = 0
best_round = 0
best = 0
for rnd in range(1, 9):
    pts = (rnd * 37) % 50 + 5
    if rnd % 4 == 0:
        pts = pts * 2
        tag = " double!"
    else:
        tag = ""
    total += pts
    if pts > best:
        best = pts
        best_round = rnd
    print(f"round {rnd}: {pts}{tag}")
    print("   " + "+" * (total // 10), total)
print("best round", best_round, "with", best, sep=" ")
