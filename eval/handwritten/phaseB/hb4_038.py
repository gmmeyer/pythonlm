# A factory conveyor between a press and a packer. The press makes a part
# every 2 ticks (every tick after tick 10). The packer takes one part every
# 3 ticks, or two if the buffer holds 4 or more. The buffer holds at most 5;
# when it is full the press stalls.
buffer = 0
made = 0
packed = 0
stalls = 0
print("conveyor")
for tick in range(1, 19):
    if tick % 2 == 0 or tick > 10:
        if buffer < 5:
            buffer += 1
            made += 1
        else:
            stalls += 1
            print("press stalls")
    if tick % 3 == 0:
        if buffer >= 4:
            buffer -= 2
            packed += 2
        elif buffer > 0:
            buffer -= 1
            packed += 1
        print(buffer)
print("made, packed, stalls")
print(made)
print(packed)
print(stalls)
