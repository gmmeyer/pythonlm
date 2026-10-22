for n in range(31, 36):
    ones = n % 10
    if ones == 1:
        o = "one"
    elif ones == 2:
        o = "two"
    elif ones == 3:
        o = "three"
    elif ones == 4:
        o = "four"
    else:
        o = "five"
    print(n, "is thirty-" + o)
