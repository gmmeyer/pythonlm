# A runner's marathon, tracked one segment at a time.
# Pace is minutes and seconds per km. Time is kept as minutes plus
# leftover seconds, carrying whole minutes over, so numbers stay small.

minutes = 0
seconds = 0
distance = 0

print("10 km at 5:20")
km = 10
distance += km
minutes += km * 5
seconds += km * 20
minutes += seconds // 60
seconds %= 60
print(minutes)
print(seconds)

print("11 km at 5:35")
km = 11
distance += km
minutes += km * 5
seconds += km * 35
minutes += seconds // 60
seconds %= 60
print(minutes)
print(seconds)

print("Water stop, 1:40")
minutes += 1
seconds += 40
minutes += seconds // 60
seconds %= 60
print(minutes)
print(seconds)

print("12 km at 6:05")
km = 12
distance += km
minutes += km * 6
seconds += km * 5
minutes += seconds // 60
seconds %= 60
print(minutes)
print(seconds)

print("9 km at 6:50")
km = 9
distance += km
minutes += km * 6
seconds += km * 50
minutes += seconds // 60
seconds %= 60

print("Final sprint, 48 seconds")
seconds += 48
minutes += seconds // 60
seconds %= 60

print("--- finish ---")
print(distance)
print(minutes // 60)
print(minutes % 60)
print(seconds)
