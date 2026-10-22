# squeeze a window around 50: shrink the farther end first
left = 10
right = 95
while right - left > 20:
    if 50 - left > right - 50:
        left += 5
    else:
        right -= 5
print(left)
print(right)
