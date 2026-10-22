# leap year test on some round years
for year in range(100, 501, 100):
    print(year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
print(96 % 4 == 0 and (96 % 100 != 0 or 96 % 400 == 0))
