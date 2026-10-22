# count the scalene triangles with perimeter 12 or less (sides a < b < c)
count = 0
for a in range(1, 5):
    for b in range(a + 1, 6):
        for c in range(b + 1, 8):
            if a + b > c and a + b + c <= 12:
                count += 1
print(count)
