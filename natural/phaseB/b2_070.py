# vending machine: dispense change using nickels and pennies only
change = 23
nickels = 0
pennies = 0
while change >= 5:
    change -= 5
    nickels += 1
while change > 0:
    change -= 1
    pennies += 1
print(nickels)
print(pennies)
