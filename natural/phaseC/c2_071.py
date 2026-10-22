pattern = ""
for i in range(12):
    if i % 2 == 0:
        pattern += "x"
    else:
        pattern += "o"
print(pattern)
print(pattern * 2)
