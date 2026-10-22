weight = 7
if weight <= 1:
    cost = 3
elif weight <= 5:
    cost = 3 + (weight - 1) * 2
else:
    cost = 11 + (weight - 5) * 3
print(cost)
