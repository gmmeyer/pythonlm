# garage: first 2 hours free, then 3 per hour, day maximum of 20
hours = 9
fee = 0
for h in range(1, hours + 1):
    if h > 2:
        fee += 3
if fee > 20:
    fee = 20
print(fee)
