# emptying the coin jar
quarters = 7
dimes = 12
nickels = 9
pennies = 23

cents = quarters * 25 + dimes * 10 + nickels * 5 + pennies
print(cents)
print(cents // 100)
print(cents % 100)
coins = quarters + dimes + nickels + pennies
print(coins)
print(cents >= 300)
