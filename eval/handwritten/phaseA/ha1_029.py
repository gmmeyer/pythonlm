# lemonade stand, saturday and sunday
price = 2

sat_cups = 46
sun_cups = 31
cups = sat_cups + sun_cups

lemons = 18
sugar = 7
# cups come in packs of 25 for 3 dollars
packs = (cups + 24) // 25
cup_cost = packs * 3

revenue = cups * price
costs = lemons + sugar + cup_cost
profit = revenue - costs

print("revenue")
print(revenue)
print("costs")
print(costs)
print("profit")
print(profit)

# split between me and my sister
print(profit // 2)
print(profit % 2)
