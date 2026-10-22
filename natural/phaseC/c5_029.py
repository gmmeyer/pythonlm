pattern = ""
for i in range(9):
    if i % 2 == 0:
        pattern += "-"
    else:
        pattern += "="
print(pattern)
print("length", len(pattern))
