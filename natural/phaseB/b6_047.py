# a customer arrives every 2 minutes, the clerk finishes one every 3 minutes
queue = 0
longest = 0
for minute in range(1, 31):
    if minute % 2 == 0:
        queue += 1
    if minute % 3 == 0 and queue > 0:
        queue -= 1
    if queue > longest:
        longest = queue
print(queue)
print(longest)
