age = 14
if age < 5:
    price = 0
    kind = "free"
elif age < 13:
    price = 5
    kind = "child"
elif age < 65:
    price = 10
    kind = "adult"
else:
    price = 7
    kind = "senior"
print("Ticket type:", kind)
print("Price:", price)
