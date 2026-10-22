# A cash register hands out change greedily with coins of 25, 10, 5 and 1.
# Each customer's bill comes from x = (x * 7 + 3) % 101 and every customer
# pays with a 100 note. We count the coins and the quarters handed out.
x = 8
coins_total = 0
quarters = 0
print("cash register")
for customer in range(5):
    x = (x * 7 + 3) % 101
    change = 100 - x
    coins = 0
    while change >= 25:
        change -= 25
        coins += 1
        quarters += 1
    while change >= 10:
        change -= 10
        coins += 1
    while change >= 5:
        change -= 5
        coins += 1
    while change >= 1:
        change -= 1
        coins += 1
    coins_total += coins
    print(coins)
print("coins and quarters")
print(coins_total)
print(quarters)
