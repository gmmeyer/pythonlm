# overdraft check
balance = 20
withdrawals = 0
for amt in range(15, 100, 15):
    if balance - amt >= -30:
        balance -= amt
        withdrawals += 1
    else:
        print("denied")
print(balance)
print(withdrawals)
