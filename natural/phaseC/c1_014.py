# grocery receipt
apples = 3
apple_price = 2
bread = 1
bread_price = 4
milk = 2
milk_price = 3
total = 0
print("GROCERY MART")
print("-" * 16)
cost = apples * apple_price
total += cost
print("Apples x" + str(apples), cost, sep=": ")
cost = bread * bread_price
total += cost
print("Bread x" + str(bread), cost, sep=": ")
cost = milk * milk_price
total += cost
print("Milk x" + str(milk), cost, sep=": ")
print("-" * 16)
print("TOTAL:", total)
