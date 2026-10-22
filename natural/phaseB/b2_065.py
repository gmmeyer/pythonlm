# traffic: count cars on a road with entries and exits
cars = 0
peak = 0
for minute in range(30):
    if minute % 4 == 0:
        cars += 3
    if minute % 3 == 0 and cars > 0:
        cars -= 2
    if cars > peak:
        peak = cars
print(cars)
print(peak)
