# bursts of 4 arrive every 5 ticks, 1 leaves every tick
queue = 0
worst = 0
for tick in range(1, 21):
    if tick % 5 == 1:
        queue += 4
    if queue > 0:
        queue -= 1
    if queue > worst:
        worst = queue
print(worst)
print(queue)
