# tip options on a $36 lunch
bill = 36
for pct in range(15, 26, 5):
    tip = (bill * pct + 50) // 100   # round to the nearest dollar
    print(tip)
    print(bill + tip)

# splitting it two ways with a $7 tip, round up
each = (bill + 7 + 1) // 2
print(each)
