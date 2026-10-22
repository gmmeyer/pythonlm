# cinema hall: 5 rows of 6 seats, seats where row + seat is a multiple of 4 are sold
sold = 0
for row in range(1, 6):
    for seat in range(1, 7):
        if (row + seat) % 4 == 0:
            sold += 1
print(sold)
print(30 - sold)
