year = 800
if not year % 4 == 0:
    print("common year")
elif not year % 100 == 0:
    print("leap year")
elif year % 400 == 0:
    print("leap year")
else:
    print("common year")
