# vending machine inventory
slots = 6
sold_out = 0
stock = 4
requests = 0
while stock > 0:
    requests += 1
    if requests % 3 == 0:
        stock += 1
    stock -= 1
    if requests > 40:
        break
print(requests)
print(stock)
