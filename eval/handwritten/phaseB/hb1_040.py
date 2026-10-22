# every third house on the block: odd numbers on the left side
left = right = 0
for house in range(1, 30, 3):
    if house % 2 == 0:
        right += 1
    else:
        left += 1
print(left)
print(right)
print(left == right)
