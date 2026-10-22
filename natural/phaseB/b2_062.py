balance = 300
rate = 3
for month in range(1, 9):
    interest = balance * rate // 100
    balance += interest
    balance -= 40
    if balance < 250:
        rate = 5
print(balance)
print(rate)
