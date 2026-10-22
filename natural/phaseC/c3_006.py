for n in range(8, 19):
    if n % 3 == 0 and n % 5 == 0:
        label = "FizzBuzz"
    elif n % 3 == 0:
        label = "Fizz"
    elif n % 5 == 0:
        label = "Buzz"
    else:
        label = str(n)
    print("[", label, "]", sep="")
