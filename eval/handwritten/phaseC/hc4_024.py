# A shop receipt with prices in cents, printed as dollars and cents.
# Cents are zero-padded to two digits; every third item is 50c off.
total = 0
for k in range(5):
    if k == 0:
        item = "gum"
        cost = 125
    elif k == 1:
        item = "tea"
        cost = 249
    elif k == 2:
        item = "bun"
        cost = 180
    elif k == 3:
        item = "pen"
        cost = 99
    else:
        item = "map"
        cost = 305
    if k % 3 == 2:
        cost -= 50
        item = item + "*"
    cents = str(cost % 100)
    if len(cents) < 2:
        cents = "0" + cents
    print(item + " " * (6 - len(item)) + "$" + str(cost // 100) + "." + cents)
    total += cost
print("-" * 11)
cents = str(total % 100)
if len(cents) < 2:
    cents = "0" + cents
print("total $" + str(total // 100) + "." + cents)
print("* = 50c off")
