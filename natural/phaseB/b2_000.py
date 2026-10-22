# bank account with an overdraft check
balance = 100
declined = 0
for day in range(1, 11):
    if day % 3 == 0:
        amount = 60 + day
        if balance - amount < -20:
            declined += 1
        else:
            balance -= amount
    else:
        balance += 25
print(balance)
print(declined)
