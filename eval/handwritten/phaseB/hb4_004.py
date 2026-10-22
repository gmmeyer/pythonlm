# A shop with one clerk. Customers arrive every other minute, plus a small
# rush every 9 minutes. Serving one customer takes 3 minutes.
queue = 0
served = 0
busy = 0
longest = 0
print("shop opens")
for minute in range(16):
    if minute % 2 == 0:
        queue += 1
    if minute % 9 == 4:
        queue += 2
    if busy > 0:
        busy -= 1
        if busy == 0:
            served += 1
    if busy == 0 and queue > 0:
        queue -= 1
        busy = 3
    if queue > longest:
        longest = queue
    if minute % 4 == 3:
        print("queue length")
        print(queue)
print("served")
print(served)
print("longest queue")
print(longest)
