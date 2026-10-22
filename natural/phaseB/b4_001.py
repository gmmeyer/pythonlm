# leap years between 396 and 409
year = 396
while year <= 409:
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        print(year)
    year += 1
