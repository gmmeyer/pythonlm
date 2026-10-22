# parking garage with hourly fee
fee = 0
for hour in range(1, 9):
    if hour <= 2:
        fee += 3
    elif hour <= 5:
        fee += 2
    else:
        fee += 1
    if fee > 15:
        print("cap")
        fee = 15
        break
print(fee)
