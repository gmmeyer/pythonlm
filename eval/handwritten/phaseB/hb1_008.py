# leap year rules, checked on some early years
y = 396
while y <= 404:
    if y % 400 == 0:
        print("leap (divisible by 400)")
    elif y % 100 == 0:
        print("century, not leap")
    elif y % 4 == 0:
        print("leap")
    else:
        print(y)
    y += 1
