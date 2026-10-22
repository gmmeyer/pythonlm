for n in range(1, 13):
    if n % 3 == 0 and n % 4 == 0:
        print("Fizzbuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 4 == 0:
        print("Buzz")
    else:
        pass
print("done")
