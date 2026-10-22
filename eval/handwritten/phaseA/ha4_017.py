# A cabin on a winter night; the outside air is -18 degrees.
# Every hour the cabin loses a quarter of the difference to the outside
# (rounded down) and the stove adds its heat.

outside = -18
inside = -5
stove = 0

print("Hour 1: stove lit")
stove = 6
loss = (inside - outside) // 4
inside += stove - loss
print(inside)

print("Hour 2")
stove = 9
loss = (inside - outside) // 4
inside += stove - loss
print(inside)

print("Hour 3")
loss = (inside - outside) // 4
inside += stove - loss
print(inside)

print("Hour 4: stove out")
stove = 0
loss = (inside - outside) // 4
inside += stove - loss
print(inside)

print("Hour 5")
loss = (inside - outside) // 4
inside += stove - loss
print(inside)
# floor division and modulo of a negative temperature
print(inside // 2)
print(inside % 5)

print("Hour 6: colder wind")
outside -= 7
loss = (inside - outside) // 4
inside += stove - loss
print(inside)

print("Hour 7: stove relit")
stove = 13
loss = (inside - outside) // 4
inside += stove - loss
print(inside)

print("--- night ---")
print(-outside)
print(inside - outside)
