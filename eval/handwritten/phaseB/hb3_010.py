a = 3
b = -2
c = 0
d = 7
if a > 0:
    if b > 0:
        print(1)
    elif b == 0:
        print(2)
    else:
        if c:
            print(3)
        elif not c:
            if d % 2 == 1:
                if d > 5:
                    print(4)
                else:
                    print(5)
            else:
                print(6)
        else:
            print(7)
else:
    print(8)
print(a + b + c + d)
