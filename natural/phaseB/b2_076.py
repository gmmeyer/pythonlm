# bank: monthly fee waived if balance stays above 100
balance = 140
fees = 0
for month in range(1, 11):
    balance -= 25
    if month % 2 == 0:
        balance += 40
    if balance < 100:
        balance -= 5
        fees += 1
print(balance)
print(fees)
