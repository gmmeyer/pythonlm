# vending machine: drink costs 85 cents
drink = 85
inserted = 100
back = inserted - drink
print(back // 10)
print(back % 10 // 5)
print(back % 5)
