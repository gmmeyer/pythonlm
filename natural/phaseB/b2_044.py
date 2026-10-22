# balance after a series of transactions: deposits on odd days, fees on multiples of 4
balance = 0
for day in range(1, 17):
    if day % 2 == 1:
        balance += day * 5
    if day % 4 == 0:
        balance -= 12
print(balance)
print(balance > 100)
