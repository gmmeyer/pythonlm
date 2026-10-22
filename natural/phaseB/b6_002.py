price = 80
member = True
quantity = 4
discount = 0
if member and quantity >= 3:
    discount = 20
elif member or quantity >= 5:
    discount = 10
if price > 100 and discount > 0:
    discount += 5
final = price - price * discount // 100
print(final)
