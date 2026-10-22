# three shops pull stock from one warehouse
warehouse = 500
shop_a = shop_b = shop_c = 0

order = 120
shop_a += order
warehouse -= order
shop_b += order // 2
warehouse -= order // 2
shop_c += 75
warehouse -= 75
print("warehouse after orders")
print(warehouse)

# a week of sales
shop_a -= 98
shop_b -= 61
shop_c -= 80
print(shop_a)
print(shop_b)
print(shop_c)

# negative stock means backorders
backorders = -(shop_b + shop_c)
print("backorders")
print(backorders)

# a and c trade their counts
shop_a, shop_c = shop_c, shop_a
print(shop_a)
print(shop_c)

# restock in cases of 24: cover backorders plus 50
need = backorders + 50
cases = (need + 23) // 24
warehouse -= cases * 24
print(cases)
print(warehouse)
