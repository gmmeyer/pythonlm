# leap year rule on years 88 to 112 (100 is not a leap year here)
for year in range(88, 113, 4):
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        print(year)
    else:
        print(0)
