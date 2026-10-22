# give change for 94 cents with as few coins as possible
owed = 94
quarters = dimes = nickels = 0
while owed >= 25:
    owed -= 25
    quarters += 1
while owed >= 10:
    owed -= 10
    dimes += 1
while owed >= 5:
    owed -= 5
    nickels += 1
pennies = owed
print(quarters)
print(dimes)
print(nickels)
print(pennies)
