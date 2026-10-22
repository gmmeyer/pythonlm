# hotel: weekends (day 5 and 6 of each week) cost 90, weekdays 60
night = 0
bill = 0
while night < 9:
    day_of_week = (night + 3) % 7
    if day_of_week == 5 or day_of_week == 6:
        bill += 90
    else:
        bill += 60
    night += 1
print(bill)
