# inventory: restock to 30 whenever below 10
stock = 22
restocks = 0
for sale in range(4, 40, 4):
    stock -= sale // 2
    if stock < 10:
        stock = 30
        restocks += 1
print(stock)
print(restocks)
