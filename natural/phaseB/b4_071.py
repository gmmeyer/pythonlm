amount = 87
quarters = 0
dimes = 0
nickels = 0
while amount >= 25:
    amount -= 25
    quarters += 1
while amount >= 10:
    amount -= 10
    dimes += 1
while amount >= 5:
    amount -= 5
    nickels += 1
print(quarters)
print(dimes)
print(nickels)
print(amount)
