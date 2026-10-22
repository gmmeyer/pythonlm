# drawdown: biggest fall from a running peak
x = 50
peak = x
worst = 0
for step in range(1, 25):
    if step % 4 == 0:
        x -= 9
    else:
        x += 3
    if x > peak:
        peak = x
    drop = peak - x
    if drop > worst:
        worst = drop
print(peak)
print(worst)
