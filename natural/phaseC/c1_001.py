# coffee shop receipt
latte = 4
muffin = 3
cookie = 2
qty = 3
subtotal = latte + muffin + cookie * qty
tax = subtotal // 10
total = subtotal + tax
print("-" * 20)
print("Latte:", latte)
print("Muffin:", muffin)
print("Cookies:", cookie * qty)
print("-" * 20)
print("Subtotal:", subtotal)
print("Tax:", tax)
print("Total:", total)
