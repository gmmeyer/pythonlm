# A lemonade stand over four days. One lemon makes 3 cups,
# lemons cost 1 coin each and sugar costs 5 coins a day.
# Unsold lemonade is poured away at night.

cash = 20
price = 2

print("Day 1: sunny")
lemons = 15
sold = 30
costs = lemons + 5
income = sold * price
cash += income - costs
print(income - costs)
print(lemons * 3 - sold)
print(cash)

print("Day 2: rain")
lemons = 10
sold = 6
costs = lemons + 5
income = sold * price
cash += income - costs
print(income - costs)
print(lemons * 3 - sold)
print(cash)

print("Day 3: heat wave")
lemons = 25
sold = 75
costs = lemons + 5
income = sold * price
cash += income - costs
print(income - costs)
print(lemons * 3 - sold)
print(cash)

print("Day 4: new price")
price += 1
lemons = 20
sold = 41
costs = lemons + 5
income = sold * price
cash += income - costs
print(income - costs)
print(lemons * 3 - sold)
print(cash)

print("--- summary ---")
profit = cash - 20
print(profit)
print(profit // 4)
print(profit % 4)
