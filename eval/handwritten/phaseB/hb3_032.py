for a in range(3):
    for b in range(3):
        if a and b:
            if a == b:
                print(a * 11)
            elif a > b:
                pass
            else:
                print(a - b)
        elif a or b:
            if not a:
                print(-b)
        else:
            print(0)
