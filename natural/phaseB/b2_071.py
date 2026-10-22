# parking lot open from hour 8 to hour 18, cars come and go
cars = 0
for hour in range(8, 19):
    if hour < 10:
        cars += 6
    elif hour < 16:
        cars += 2
    else:
        cars -= 7
        if cars < 0:
            cars = 0
print(cars)
