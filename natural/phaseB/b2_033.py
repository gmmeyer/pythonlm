# fuel gauge
fuel = 60
distance = 0
while fuel > 0:
    distance += 10
    fuel -= 7
    if distance % 30 == 0:
        fuel += 5
print(distance)
print(fuel)
