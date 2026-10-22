# staircase robot: climbs 2, slips back 1 every third step
height = 0
step = 0
while height < 20:
    step += 1
    height += 2
    if step % 3 == 0:
        height -= 1
print(step)
print(height)
