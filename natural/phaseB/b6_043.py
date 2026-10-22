fuel = 40
refuels = 0
distance = 0
for leg in range(1, 13):
    need = 8 + leg % 4 * 2
    if fuel < need:
        fuel = 40
        refuels += 1
    fuel -= need
    distance += need * 5
print(distance)
print(refuels)
print(fuel)
