price = 80
qty = 4
subtotal = price * qty
if subtotal > 200:
    discount = subtotal // 10
else:
    discount = 0
total = subtotal - discount
print("== ORDER ==")
print("Subtotal:", subtotal)
print("Discount:", discount)
print("Total:", total)
