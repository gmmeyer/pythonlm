# pseudo-random dice rolls (1 to 6)
x = 42
ones = 0
sixes = 0
for roll in range(20):
    x = (x * 7 + 3) % 101
    face = x % 6 + 1
    if face == 1:
        ones += 1
    elif face == 6:
        sixes += 1
print(ones)
print(sixes)
