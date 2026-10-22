# bank balance with a monthly deposit and a withdrawal limit
balance = 100
month = 0
while balance < 400:
    month += 1
    balance += 60
    if month % 3 == 0:
        balance -= 40
    print(balance)
print(month)
