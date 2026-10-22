# receipt with right-aligned amounts
print("ITEM        QTY  COST")
name = "pens"
qty = 12
cost = 18
print(name + " " * (12 - len(name)) + str(qty) + " " * (5 - len(str(qty))) + " " * (4 - len(str(cost))) + str(cost))
name = "notebook"
qty = 3
cost = 9
print(name + " " * (12 - len(name)) + str(qty) + " " * (5 - len(str(qty))) + " " * (4 - len(str(cost))) + str(cost))
name = "tape"
qty = 1
cost = 150
print(name + " " * (12 - len(name)) + str(qty) + " " * (5 - len(str(qty))) + " " * (4 - len(str(cost))) + str(cost))
print("=" * 21)
