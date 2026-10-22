# loan: 2% interest each month, fixed installment of 80
balance = 500
payment = 80
months = 0
while balance > 0:
    interest = balance // 50
    balance = balance + interest - payment
    months += 1
    if balance < 0:
        balance = 0
print(months)
print(balance)
