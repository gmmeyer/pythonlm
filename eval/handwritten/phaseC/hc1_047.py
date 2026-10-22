price = 65
paid = 0
coin = 25
while paid < price:
    paid += coin
    print("inserted", coin, "-> total", paid)
    if coin == 25:
        coin = 10
    else:
        coin = 25
change = paid - price
print("dispensing: crisps")
if change > 0:
    print(f"change: {change}c")
else:
    print("exact money, thanks")
