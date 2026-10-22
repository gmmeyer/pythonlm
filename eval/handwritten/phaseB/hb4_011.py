# A savings account over one year. Each month a deposit of 15 arrives,
# then interest of 1 for every full 25 in the account. A big purchase in
# month 7 drains the account, and a fee hits when the balance is under 50.
balance = 30
fees = 0
print("savings year")
for month in range(1, 13):
    balance += 15
    interest = balance // 25
    balance += interest
    if month == 7:
        balance -= 120
        print("bought a bike")
    if balance < 50:
        balance -= 3
        fees += 3
        print("low balance fee")
    print(balance)
print("fees paid")
print(fees)
print(balance >= 100)
