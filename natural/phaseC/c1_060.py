# dice histogram from a simple sequence
x = 3
f1 = f2 = f3 = f4 = f5 = f6 = 0
for roll in range(20):
    x = (x * 5 + 3) % 17
    face = x % 6 + 1
    if face == 1:
        f1 += 1
    elif face == 2:
        f2 += 1
    elif face == 3:
        f3 += 1
    elif face == 4:
        f4 += 1
    elif face == 5:
        f5 += 1
    else:
        f6 += 1
print("1", "#" * f1)
print("2", "#" * f2)
print("3", "#" * f3)
print("4", "#" * f4)
print("5", "#" * f5)
print("6", "#" * f6)
