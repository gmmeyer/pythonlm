# A stock price wanders according to x = (x * 7 + 3) % 101.
# The trader buys one share whenever the price dips below 47 and sells
# every share once it climbs above 55.
price = 50
cash = 200
shares = 0
x = 5
print("trading days")
for day in range(15):
    x = (x * 7 + 3) % 101
    price += x % 11 - 5
    if price < 47 and cash >= price:
        cash -= price
        shares += 1
        print("buy")
    elif price > 55 and shares > 0:
        cash += price * shares
        shares = 0
        print("sell")
    print(price)
print("cash and shares")
print(cash)
print(shares)
