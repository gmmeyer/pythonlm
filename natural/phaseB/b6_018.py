# cinema tickets by age and day
weekend = True
for age in range(5, 71, 13):
    if age < 12:
        price = 6
    elif age >= 65:
        price = 7
    elif weekend:
        price = 12
    else:
        price = 10
    print(age)
    print(price)
