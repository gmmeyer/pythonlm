item_a = "apples"
item_b = "bread"
item_c = "milk"
price_a = 3
price_b = 4
price_c = 2
qty_a = 5
qty_c = 2
line_a = price_a * qty_a
line_c = price_c * qty_c
total = line_a + price_b + line_c
print("CORNER SHOP")
print("-" * 22)
print(item_a + " x" + str(qty_a), line_a, sep=" ..... ")
print(item_b + " x1", price_b, sep=" ..... ")
print(item_c + " x" + str(qty_c), line_c, sep=" ..... ")
print("-" * 22)
print("TOTAL", total, sep=": ")
print("thank you!")
