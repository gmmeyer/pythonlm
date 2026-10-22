# ATM: dispense bills of 50, 20 and 10
amount = 180
fifties = 0
twenties = 0
tens = 0
while amount >= 50:
    amount -= 50
    fifties += 1
while amount >= 20:
    amount -= 20
    twenties += 1
while amount >= 10:
    amount -= 10
    tens += 1
print(fifties)
print(twenties)
print(tens)
print(amount == 0)
