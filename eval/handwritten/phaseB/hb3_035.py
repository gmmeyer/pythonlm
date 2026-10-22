n = 0
while n < 8:
    n += 1
    if n % 2 == 0:
        if n % 4 == 0:
            if n == 8:
                print(800)
            else:
                pass
        else:
            print(n * 10)
    elif n > 4:
        print(-n)
    else:
        pass
print(n)
