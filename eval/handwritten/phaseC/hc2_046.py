codes = ""
for i in range(1, 21):
    if i % 15 == 0:
        codes += "X"
    elif i % 3 == 0:
        codes += "F"
    elif i % 5 == 0:
        codes += "B"
    else:
        codes += str(i % 10)
print(codes)
