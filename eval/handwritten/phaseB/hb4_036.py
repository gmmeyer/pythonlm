# A rabbit hops on a line between fences at 0 and 15. Each hop draws
# x = (x * 7 + 3) % 101: even draws hop right, odd draws hop left, and the
# hop is 1 + x % 3 long. Hitting a fence bounces it back inside.
x = 13
pos = 7
far_right = 7
print("rabbit hops")
for hop in range(18):
    x = (x * 7 + 3) % 101
    length = 1 + x % 3
    if x % 2 == 0:
        pos += length
    else:
        pos -= length
    if pos > 15:
        pos = 30 - pos
        print("bounce off east fence")
    elif pos < 0:
        pos = -pos
        print("bounce off west fence")
    if pos > far_right:
        far_right = pos
    print(pos)
print("furthest east")
print(far_right)
