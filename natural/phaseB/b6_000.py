# shipping cost by parcel weight (kg)
weight = 7
if weight <= 1:
    cost = 5
elif weight <= 5:
    cost = 9
elif weight <= 10:
    cost = 15
else:
    cost = 15 + (weight - 10) * 2
print(cost)
