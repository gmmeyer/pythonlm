# vending machine: customer inserts 25s until the snack price is covered
price = 85
inserted = 0
coins = 0
while inserted < price:
    inserted += 25
    coins += 1
change = inserted - price
print(coins)
print(change)
if change > 0:
    print("take your change")
else:
    print("exact amount")
