# making change for 187 cents
cents = 187
quarters = cents // 25
cents %= 25
dimes = cents // 10
cents %= 10
nickels = cents // 5
pennies = cents % 5
print(quarters)
print(dimes)
print(nickels)
print(pennies)
