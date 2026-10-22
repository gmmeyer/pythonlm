# A week of trading one stock. The price moves every day, sometimes
# down. We buy and sell whole shares only, starting with 600 coins.

price = 48
cash = 600
shares = 0
spent = 0

print("Monday: buy 10")
shares += 10
spent += 10 * price
cash -= 10 * price
print(cash)

print("Tuesday")
change = -6
price += change
print(price)
print(shares * price)

print("Wednesday: buy the dip")
change = -9
price += change
spent += 3 * price
cash -= 3 * price
shares += 3
print(price)
print(cash)
print(shares * price)

print("Thursday")
change = 17
price += change
print(price)
print(shares * price)

print("Friday: sell everything")
change = -2
price += change
cash += shares * price
print(price)
print(cash)

print("--- week ---")
# average price paid per share
print(spent // shares)
shares = 0
gain = cash - 600
print(gain)
# 1 percent of 600 is 6
print(gain // 6)
print(gain % 6)
