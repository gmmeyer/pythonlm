# two counters moving toward each other until they cross
left = 1
right = 50
steps = 0
while left < right:
    left *= 2
    right -= 5
    steps += 1
    print(left)
    print(right)
print(steps)
