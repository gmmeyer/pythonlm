# A sunflower's height in millimeters, measured once a week.
# It grows by a fifth of its height plus 12 mm, and every second week
# a caterpillar eats (height % 9) mm off the top.

height = 40

print("Week 1")
height += height // 5 + 12
print(height)

print("Week 2")
height += height // 5 + 12
height -= height % 9
print(height)

print("Week 3")
height += height // 5 + 12
print(height)

print("Week 4")
height += height // 5 + 12
height -= height % 9
print(height)

print("Week 5")
height += height // 5 + 12
print(height)

print("Week 6")
height += height // 5 + 12
height -= height % 9
print(height)

print("Week 7: tied to a stake")
# with support it grows twice as fast this week
height += (height // 5 + 12) * 2
print(height)

print("Week 8")
height += height // 5 + 12
height -= height % 9
print(height)

print("Week 9: storm")
# the storm bends it; it loses a quarter of its height
height -= height // 4
print(height)

print("--- in centimeters ---")
print(height // 10)
print(height % 10)
print(height - 40)
