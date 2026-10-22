# fitness: heart rate zone for each minute of a workout
rate = 90
easy = 0
hard = 0
for minute in range(1, 21):
    if minute <= 10:
        rate += 6
    else:
        rate -= 4
    if rate >= 130:
        hard += 1
    elif rate < 110:
        easy += 1
print(rate)
print(easy)
print(hard)
