# A parking lot with 25 spaces over a working day in half-hour slots.
# Mornings bring many arrivals, midday is balanced, evenings empty out.
# Cars that find the lot full are turned away.
cars = 3
capacity = 25
turned_away = 0
print("parking lot")
for slot in range(16):
    arrive = 0
    leave = 0
    if slot < 6:
        arrive = 4
    elif slot < 11:
        arrive = 1
        leave = 1
    else:
        leave = 5
    if slot % 4 == 1:
        arrive += 2
    cars -= leave
    if cars < 0:
        cars = 0
    cars += arrive
    if cars > capacity:
        turned_away += cars - capacity
        cars = capacity
        print("lot full")
    if slot % 3 == 2:
        print(cars)
print("turned away")
print(turned_away)
print(cars)
