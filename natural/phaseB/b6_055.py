limit = 600
load = 0
riders = 0
turned_away = 0
for person in range(1, 11):
    weight = 55 + person * 4
    if load + weight <= limit:
        load += weight
        riders += 1
    else:
        turned_away += 1
print(riders)
print(turned_away)
print(load)
