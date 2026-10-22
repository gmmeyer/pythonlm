n = 7
while n < 200:
    print("ID-" + "0" * (5 - len(str(n))) + str(n))
    n = n * 6
