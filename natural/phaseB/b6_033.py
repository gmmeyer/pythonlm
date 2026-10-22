kwh = 340
bill = 0
if kwh > 300:
    bill += (kwh - 300) * 3
    kwh = 300
if kwh > 100:
    bill += (kwh - 100) * 2
    kwh = 100
bill += kwh
print(bill)
