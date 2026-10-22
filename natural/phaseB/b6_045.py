balance = 300
refused = 0
withdrawals = 0
for n in range(1, 9):
    amount = n * 20
    if amount <= balance:
        balance -= amount
        withdrawals += 1
    else:
        refused += 1
print(balance)
print(withdrawals)
print(refused)
