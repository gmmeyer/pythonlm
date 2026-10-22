ruler = ""
for i in range(31):
    if i % 10 == 0:
        ruler += "|"
    elif i % 5 == 0:
        ruler += "+"
    else:
        ruler += "-"
print(ruler)
print("0" + " " * 9 + "1" + " " * 9 + "2" + " " * 9 + "3")
