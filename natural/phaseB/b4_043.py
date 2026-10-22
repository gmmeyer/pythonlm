# savings grow 10% a year plus a 5 deposit
balance = 100
years = 0
while balance < 200:
    balance = balance + balance // 10 + 5
    years += 1
print(years)
print(balance)
