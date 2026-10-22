# parking lot counter
capacity = 5
cars = 0
turned_away = 0
for event in range(1, 21):
    if event % 3 == 0 and cars > 0:
        cars -= 1
    else:
        if cars < capacity:
            cars += 1
        else:
            turned_away += 1
print(cars)
print(turned_away)
print(cars == capacity)
