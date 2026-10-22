item1 = "tea"
item2 = "sandwich"
item3 = "cookie"
p1 = 3
p2 = 8
p3 = 2
for step in range(3):
    if step == 0:
        name = item1
        price = p1
    elif step == 1:
        name = item2
        price = p2
    else:
        name = item3
        price = p3
    print(name + "." * (14 - len(name)) + str(price))
print("=" * 15)
print("total", p1 + p2 + p3)
