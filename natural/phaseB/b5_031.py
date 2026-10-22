# a shop queue with random-ish arrivals and one served per tick
x = 17
queue = 0
peak = 0
served = 0
for tick in range(25):
    x = (x * 13 + 7) % 64
    if x % 4 != 0:
        queue += 1
    if queue > 0:
        queue -= 1
        served += 1
    if queue > peak:
        peak = queue
print(queue)
print(peak)
print(served)
