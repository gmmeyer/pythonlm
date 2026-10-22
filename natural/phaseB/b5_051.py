a = 4
b = -9
c = 2
if a > 0 and b > 0 and c > 0:
    print("all positive")
elif a <= 0 or b <= 0 or c <= 0:
    print("at least one bad side")
print(not (a > 0 and b > 0 and c > 0))
