for age in range(0, 80, 12):
    if age < 5:
        kind = "free"
        price = 0
    elif age < 18:
        kind = "youth"
        price = 6
    elif age < 65:
        kind = "adult"
        price = 10
    else:
        kind = "senior"
        price = 7
    print(f"age {age}: {kind} ticket costs {price}")
