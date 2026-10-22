# A lighthouse flashes groups of flashes. Each group is a number whose
# digits (lowest first) are flash lengths in ticks. There is one dark tick
# after every flash and three dark ticks after every group.
lit = 0
dark = 0
tick = 0
print("lighthouse")
for group in range(3):
    pattern = 213
    if group == 1:
        pattern = 132
    while pattern > 0:
        length = pattern % 10
        pattern //= 10
        print("flash")
        print(length)
        for t in range(length):
            tick += 1
            lit += 1
        tick += 1
        dark += 1
    tick += 3
    dark += 3
    print("group done at tick")
    print(tick)
print(lit)
print(dark)
print(lit * 10 // tick)
