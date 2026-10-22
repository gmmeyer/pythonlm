# group of visitors, ages 0, 20, 40, 60, 80
total = 0
for age in range(0, 100, 20):
    if age < 5:
        price = 0
    elif age < 13:
        price = 6
    elif age < 65:
        price = 12
    else:
        price = 8
    total += price
    print(price)
print("Total:")
print(total)
