# queue: one arrival every 2 ticks, one departure every 3 ticks
queue = 0
longest = 0
for tick in range(1, 31):
    if tick % 2 == 0:
        queue += 1
    if tick % 3 == 0 and queue > 0:
        queue -= 1
    if queue > longest:
        longest = queue
print(queue)
print(longest)
