# income tax: nothing on the first 100, 10% up to 300, 25% above that
income = 420
if income <= 100:
    tax = 0
elif income <= 300:
    tax = (income - 100) * 10 // 100
else:
    tax = 20 + (income - 300) * 25 // 100
print(tax)
print(income - tax)
