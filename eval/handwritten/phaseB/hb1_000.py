# Movie night: ticket prices for a family of five.
# Under 3 free, 3-12 child, 13-64 adult, 65+ senior.

total = 0
for k in range(5):
    age = 67 - k * 15
    if age < 3:
        price = 0
    elif age <= 12:
        price = 8
    elif age < 65:
        price = 13
    else:
        price = 9
    print(price)
    total += price

print(total)
if total > 40:
    print("buy the family pass instead")
