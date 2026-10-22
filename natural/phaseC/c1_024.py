# right-align numbers in a column
v = 1
print("values")
print("======")
while v < 300:
    print(" " * (6 - len(str(v))) + str(v))
    v = v * 2 + 1
