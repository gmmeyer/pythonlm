# count leap years, using the full Gregorian rule (years 196..204)
leap = 0
for year in range(196, 205):
    if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
        leap += 1
        print(year)
print(leap)
