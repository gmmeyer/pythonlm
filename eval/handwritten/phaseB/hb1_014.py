# shipping cost (dollars) by package weight (ounces)
for weight in range(4, 80, 15):
    if weight <= 8:
        cost = 4
    elif weight <= 16:
        cost = 6
    elif weight <= 48:
        cost = 6 + (weight - 16) // 8
    else:
        cost = 12
    print(cost)
