n = 305
h = n // 100
rest = n % 100
if h == 1:
    hw = "one"
elif h == 2:
    hw = "two"
elif h == 3:
    hw = "three"
else:
    hw = "many"
text = hw + " hundred"
if rest > 0:
    text = text + " and " + str(rest)
print(n, "is", text)
