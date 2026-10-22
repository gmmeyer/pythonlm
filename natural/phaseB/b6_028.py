stock = 50
orders = 0
low_days = 0
for day in range(1, 31):
    stock -= 4 + day % 3
    if stock < 20:
        low_days += 1
        stock += 40
        orders += 1
print(stock)
print(orders)
print(low_days)
