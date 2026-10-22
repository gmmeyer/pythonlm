# A traffic light repeats a 90 second cycle: green for seconds 0-39,
# yellow 40-44, red 45-89. For cars arriving at different times we find
# their place in the cycle and the wait until the next green.
# phase // 45 is 1 during red and 0 otherwise.

cycle = 90

print("Car at 130 s")
t = 130
phase = t % cycle
print(phase)
print(phase // 45)
print((cycle - phase) % cycle)

print("Car at 267 s")
t = 267
phase = t % cycle
print(phase)
print(phase // 45)
print((cycle - phase) % cycle)

print("Car at 360 s")
t = 360
phase = t % cycle
print(phase)
print(phase // 45)
print((cycle - phase) % cycle)

print("Car at 538 s")
t = 538
phase = t % cycle
print(phase)
print(phase // 45)
print((cycle - phase) % cycle)

print("New timing: 75 second cycle")
cycle = 75

print("Car at 538 s again")
phase = t % cycle
print(phase)
print((cycle - phase) % cycle)

print("Car at 989 s")
t = 989
phase = t % cycle
print(phase)
print((cycle - phase) % cycle)
print(t // cycle)
