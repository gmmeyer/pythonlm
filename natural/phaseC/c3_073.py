sales1 = 5
sales2 = 9
sales3 = 3
print("Mon", "*" * sales1)
print("Tue", "*" * sales2)
print("Wed", "*" * sales3)
best = "Mon"
top = sales1
if sales2 > top:
    best = "Tue"
    top = sales2
if sales3 > top:
    best = "Wed"
    top = sales3
print("Best day:", best, "with", top)
