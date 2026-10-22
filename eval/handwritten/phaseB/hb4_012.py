# A vending machine fed with coins. Coins come from the digits of a few
# numbers (lowest digit first): 1 = dime, 2 = quarter, 5 = dollar.
# A snack costs 65. Once credit covers the price it vends and returns change.
credit = 0
vended = 0
change_total = 0
print("vending machine ready")
for bag in range(3):
    if bag == 0:
        coins = 221
    elif bag == 1:
        coins = 512
    else:
        coins = 122
    while coins > 0:
        c = coins % 10
        coins //= 10
        if c == 1:
            credit += 10
        elif c == 2:
            credit += 25
        else:
            credit += 100
        if credit >= 65:
            vended += 1
            change = credit - 65
            change_total += change
            credit = 0
            print("vend, change")
            print(change)
    print("credit left")
    print(credit)
print("snacks sold")
print(vended)
print(change_total)
