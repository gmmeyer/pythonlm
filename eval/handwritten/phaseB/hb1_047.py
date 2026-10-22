# income in hundreds of dollars; first 100 untaxed, 15% to 400, 30% above
for income in range(60, 700, 120):
    tax = 0
    if income > 100:
        if income > 400:
            tax += (income - 400) * 3 // 10
            mid = 300
        else:
            mid = income - 100
        tax += mid // 20 * 3
    print(tax)
    print(income - tax)
