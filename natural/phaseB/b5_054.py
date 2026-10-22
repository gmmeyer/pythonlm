# running maximum gap between consecutive readings
x = 9
prev = x
gap = 0
for i in range(15):
    x = (x * 7 + 11) % 50
    d = x - prev
    if d < 0:
        d = -d
    if d > gap:
        gap = d
    prev = x
print(gap)
print(prev)
