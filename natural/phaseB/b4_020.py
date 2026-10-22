passing = 0
for score in range(55, 100, 10):
    if score >= 90:
        print("A")
        passing += 1
    elif score >= 80:
        print("B")
        passing += 1
    elif score >= 70:
        print("C")
        passing += 1
    elif score >= 60:
        print("D")
        passing += 1
    else:
        print("F")
print(passing)
