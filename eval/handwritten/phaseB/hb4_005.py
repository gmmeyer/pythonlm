# A ball bounces between walls at 0 and 30. At each wall it reflects and
# loses one unit of speed. Stop when it is at rest or time runs out.
pos = 4
vel = 6
low = 0
high = 30
bounces = 0
ticks = 0
print("bouncing ball")
while vel != 0 and ticks < 28:
    ticks += 1
    pos += vel
    if pos > high:
        pos = high - (pos - high)
        vel = -vel + 1
        bounces += 1
        print("bounce high")
        print(pos)
    elif pos < low:
        pos = low - pos
        vel = -vel - 1
        bounces += 1
        print("bounce low")
        print(pos)
print("bounces")
print(bounces)
print("final position")
print(pos)
print(vel)
