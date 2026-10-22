# parking lot with 5 spaces: arrivals who find it full are turned away
x = 21
cars = 0
turned_away = 0
for step in range(40):
    x = (x * 21 + 5) % 32
    if x % 3 != 0:
        if cars < 5:
            cars += 1
        else:
            turned_away += 1
    elif cars > 0:
        cars -= 1
print(cars)
print(turned_away)
