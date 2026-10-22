seats = 12
booked = 0
refused = 0
for request in range(1, 9):
    party = 1 + request % 4
    if booked + party <= seats:
        booked += party
    else:
        refused += 1
print(booked)
print(refused)
