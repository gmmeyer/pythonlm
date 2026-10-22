# robot on a number line bouncing between walls at 0 and 10
pos = 4
direction = 1
bounces = 0
for step in range(25):
    pos += direction * 3
    if pos >= 10:
        pos = 10
        direction = -1
        bounces += 1
    elif pos <= 0:
        pos = 0
        direction = 1
        bounces += 1
print(pos)
print(bounces)
