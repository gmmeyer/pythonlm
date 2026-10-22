# change from a 10 dollar bill
paid = 900
price = 637
change = paid - price
quarters = change // 25
change = change % 25
dimes = change // 10
change %= 10
nickels = change // 5
pennies = change % 5
print(quarters)
print(dimes)
print(nickels)
print(pennies)
