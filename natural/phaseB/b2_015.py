# savings with interest and a withdrawal limit
balance = 200
month = 0
while month < 12:
    month += 1
    balance += balance // 20
    if month % 4 == 0:
        balance -= 60
    if balance < 100:
        print("low")
        break
print(balance)
print(month)
