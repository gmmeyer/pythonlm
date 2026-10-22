budget = 60
spent = 0
items = 0
price = 7
while True:
    if spent + price > budget:
        break
    spent += price
    items += 1
    price += 2      # each thing on the list costs a bit more
print(items)
print(spent)
print(budget - spent)
