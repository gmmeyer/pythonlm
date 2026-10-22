for month in range(1, 13):
    if month == 12 or month <= 2:
        season = "winter"
    elif month <= 5:
        season = "spring"
    elif month <= 8:
        season = "summer"
    else:
        season = "autumn"
    print(f"Month {month}: {season}")
