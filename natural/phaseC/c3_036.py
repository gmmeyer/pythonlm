budget = 50
spent = 0
item = "book"
price = 18
for i in range(4):
    if spent + price <= budget:
        spent += price
        print("Bought", item, i + 1, "- spent", spent)
    else:
        print("Cannot afford another", item)
        break
print("Left:", budget - spent)
