n = 750
text = ""
while n > 0:
    d = n % 16
    if d == 10:
        text = "A" + text
    elif d == 11:
        text = "B" + text
    elif d == 12:
        text = "C" + text
    elif d == 13:
        text = "D" + text
    elif d == 14:
        text = "E" + text
    elif d == 15:
        text = "F" + text
    else:
        text = str(d) + text
    n = n // 16
print("750 in hex is", text)
