# vending machine: item costs 35, insert coins until enough
cost = 35
inserted = 0
coin = 10
presses = 0
while inserted < cost:
    inserted += coin
    presses += 1
    if presses == 2:
        coin = 5
print(inserted)
print(inserted - cost)
print(presses)
