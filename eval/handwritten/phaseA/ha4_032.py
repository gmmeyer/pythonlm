# A river ferry carries at most 14 cars. Cars queue on the north bank.
# Branch-free trick: while the queue is shorter than 28 cars,
#   carried = queue - queue // 14 * (queue - 14)
# gives 14 for a long queue and the whole queue for a short one.
# A round trip (over and back) takes 50 minutes.

queue = 37
capacity = 14
crossings = 0
minutes = 0

print("Crossing 1")
# the queue is far longer than the boat: it leaves full
carried = capacity
queue -= carried
crossings += 1
minutes += 50
print(queue)

print("Crossing 2")
carried = queue - queue // capacity * (queue - capacity)
queue -= carried
crossings += 1
minutes += 50
print(carried)
print(queue)

print("Six more cars arrive")
queue += 6
print(queue)

print("Crossing 3")
carried = queue - queue // capacity * (queue - capacity)
queue -= carried
crossings += 1
minutes += 50
print(carried)
print(queue)

print("Crossing 4")
carried = queue - queue // capacity * (queue - capacity)
queue -= carried
crossings += 1
minutes += 50
print(carried)
print(queue)

print("--- morning ---")
print(crossings)
print(minutes // 60)
print(minutes % 60)
