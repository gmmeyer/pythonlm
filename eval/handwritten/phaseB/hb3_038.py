a = 100
b = 1
while a > b:
    a //= 2
    b *= 3
    if a == b:
        print("eq")
    elif a < b:
        print("crossed")
print(a)
print(b)
