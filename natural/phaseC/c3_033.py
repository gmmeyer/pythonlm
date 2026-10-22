shirt = 25
shoes = 40
hat = 12
total = shirt + shoes + hat
print("Subtotal:", total)
if total > 70:
    discount = total // 10
    print("Discount:", discount)
    total = total - discount
else:
    print("No discount")
print("You pay", total)
