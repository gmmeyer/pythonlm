# inventory restocking: reorder when stock falls below threshold
stock = 40
reorders = 0
for day in range(20):
    sold = 3 + day % 5
    stock -= sold
    if stock < 15:
        stock += 50
        reorders += 1
        print("restock")
print(stock)
print(reorders)
