x = "mango"
y = "apple"
z = "cherry"
if x > y:
    x, y = y, x
if y > z:
    y, z = z, y
if x > y:
    x, y = y, x
print(x, y, z, sep=" < ")
