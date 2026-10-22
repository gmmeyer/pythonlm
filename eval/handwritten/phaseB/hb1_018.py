# vending machine, snack costs $1.35
price = 135
paid = 0
coin = 25
while paid < price:
    paid += coin
    if paid == 100:
        coin = 10    # out of quarters, switching to dimes
print(paid)
change = paid - price
print(change)
print(change == 0)
