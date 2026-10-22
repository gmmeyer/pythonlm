# which month has 100 days into the year? (non-leap year)
day = 100
month = 1
while True:
    if month == 2:
        length = 28
    elif month == 4 or month == 6 or month == 9 or month == 11:
        length = 30
    else:
        length = 31
    if day <= length:
        break
    day -= length
    month += 1
print(month)
print(day)
