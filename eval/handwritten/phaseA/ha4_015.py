# A circular bus line with 9 stops, numbered 0 to 8.
# Bus A drives clockwise 4 stops per leg, bus B counter-clockwise 2 stops.
# The gap is how many stops A would have to drive forward to reach B.

bus_a = 0
bus_b = 0
laps_a = 0

print("Leg 1")
laps_a += (bus_a + 4) // 9
bus_a = (bus_a + 4) % 9
bus_b = (bus_b - 2) % 9
print(bus_a)
print(bus_b)
print((bus_b - bus_a) % 9)

print("Leg 2")
laps_a += (bus_a + 4) // 9
bus_a = (bus_a + 4) % 9
bus_b = (bus_b - 2) % 9
print(bus_a)
print(bus_b)
print((bus_b - bus_a) % 9)

print("Drivers swap buses")
bus_a, bus_b = bus_b, bus_a
print(bus_a)
print(bus_b)

print("Leg 3")
laps_a += (bus_a + 4) // 9
bus_a = (bus_a + 4) % 9
bus_b = (bus_b - 2) % 9
print((bus_b - bus_a) % 9)

print("Leg 4")
laps_a += (bus_a + 4) // 9
bus_a = (bus_a + 4) % 9
bus_b = (bus_b - 2) % 9
print((bus_b - bus_a) % 9)

print("Leg 5")
laps_a += (bus_a + 4) // 9
bus_a = (bus_a + 4) % 9
bus_b = (bus_b - 2) % 9
print((bus_b - bus_a) % 9)

print("--- end of shift ---")
print(bus_a)
print(bus_b)
print(laps_a)
