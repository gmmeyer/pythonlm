# A clock hand on a dial of 12 positions, numbered 0 to 11.
# Every tick the hand jumps forward and wraps around with % 12.
# We also count laps: how many times the hand went past 0.

position = 0
laps = 0
step = 7

print("tick 1")
laps += (position + step) // 12
position = (position + step) % 12
print(position)

print("tick 2")
laps += (position + step) // 12
position = (position + step) % 12
print(position)

print("tick 3")
laps += (position + step) // 12
position = (position + step) % 12
print(position)

print("tick 4")
laps += (position + step) // 12
position = (position + step) % 12
print(position)

print("tick 5")
laps += (position + step) // 12
position = (position + step) % 12
print(position)
print(laps)

print("The hand now runs backwards, 5 at a time")
step = -5

print("tick 6")
laps += (position + step) // 12
position = (position + step) % 12
print(position)

print("tick 7")
laps += (position + step) // 12
position = (position + step) % 12
print(position)

print("tick 8")
laps += (position + step) // 12
position = (position + step) % 12
print(position)

print("tick 9")
laps += (position + step) // 12
position = (position + step) % 12
print(position)

print("--- summary ---")
print(laps)
print(position)
