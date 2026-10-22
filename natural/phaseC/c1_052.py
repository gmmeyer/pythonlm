# inventory report
print("item", "qty", "value", sep=" | ")
print("-" * 22)
total = 0
qty = 12
unit = 3
print("bolts", qty, qty * unit, sep=" | ")
total += qty * unit
qty = 5
unit = 9
print("nuts", qty, qty * unit, sep=" | ")
total += qty * unit
qty = 20
unit = 2
print("washers", qty, qty * unit, sep=" | ")
total += qty * unit
print("-" * 22)
print("total value:", total)
