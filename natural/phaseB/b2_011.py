# vending machine giving change
price = 65
paid = 100
change = paid - price
coins = 0
while change > 0:
    if change >= 25:
        change -= 25
    elif change >= 10:
        change -= 10
    elif change >= 5:
        change -= 5
    else:
        change -= 1
    coins += 1
print(coins)
