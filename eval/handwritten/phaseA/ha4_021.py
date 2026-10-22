# A robot vacuum on a 10 by 8 grid that wraps around at the edges:
# leaving on the right brings it back on the left, and so on.
# Every move cleans one cell per step travelled.

x = 3
y = 2
cleaned = 0

print("East 5")
x = (x + 5) % 10
cleaned += 5
print(x)
print(y)

print("South 3")
# south means y goes down; below 0 it wraps to the top row
y = (y - 3) % 8
cleaned += 3
print(x)
print(y)

print("East 9")
x = (x + 9) % 10
cleaned += 9
print(x)
print(y)

print("West 12")
x = (x - 12) % 10
cleaned += 12
print(x)
print(y)

print("Diagonal 4")
x = (x + 4) % 10
y = (y + 4) % 8
cleaned += 4
print(x)
print(y)

print("Map turned sideways")
# the owner rotates the map, so x and y trade places
x, y = y, x
x %= 10
y %= 8
print(x)
print(y)

print("--- report ---")
print(y * 10 + x)
print(cleaned)
print(80 - cleaned)
