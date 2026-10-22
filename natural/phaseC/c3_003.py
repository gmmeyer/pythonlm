for n in range(1, 13):
    if n % 3 == 0 and n % 4 == 0:
        print(f"{n} is both")
    elif n % 3 == 0:
        print(f"{n} is three")
    elif n % 4 == 0:
        print(f"{n} is four")
    else:
        print(f"{n} is plain")
