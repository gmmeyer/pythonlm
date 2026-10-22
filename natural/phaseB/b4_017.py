# income in thousands, brackets at 40 and 80
income = 85
tax = 0
if income > 80:
    tax += (income - 80) * 30 // 100
    income = 80
if income > 40:
    tax += (income - 40) * 20 // 100
    income = 40
tax += income * 10 // 100
print(tax)
