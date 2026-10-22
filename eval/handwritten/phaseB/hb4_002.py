# An ant walks around a ring of 13 cells. Its stride changes depending on
# the cell it lands on: multiples of 3 speed it up, multiples of 5 slow it
# down. Position wraps around the ring with the modulo operator.
ring = 13
pos = 0
stride = 1
visits_zero = 0
print("ant on a ring")
for step in range(1, 21):
    pos = (pos + stride) % ring
    if pos % 3 == 0:
        stride += 1
    elif pos % 5 == 0:
        stride -= 1
    if stride > 6:
        stride = 1
    if stride < 1:
        stride = 4
    if pos == 0:
        visits_zero += 1
        print("back at start")
    if step % 5 == 0:
        print(pos)
print("times at cell zero")
print(visits_zero)
print(stride)
