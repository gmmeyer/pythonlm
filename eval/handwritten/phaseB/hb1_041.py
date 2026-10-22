balance = 730
payment = 85
month = 0
while balance > 0:
    month += 1
    balance += balance // 50       # 2% interest a month, rounded down
    if balance < payment:
        print(balance)             # last payment is smaller
        balance = 0
    else:
        balance -= payment
print(month)
