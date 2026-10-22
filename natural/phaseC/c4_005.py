width = 12
name = "tea"
price = 2
print(name + " " * (width - len(name)) + str(price))
name = "bagel"
price = 4
print(name + " " * (width - len(name)) + str(price))
name = "soup"
price = 7
print(name + " " * (width - len(name)) + str(price))
print("-" * (width + 1))
print("total" + " " * (width - 5) + str(2 + 4 + 7))
