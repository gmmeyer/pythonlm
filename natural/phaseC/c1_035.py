for n in range(1, 16):
    if n % 15 == 0:
        word = "FizzBuzz"
    elif n % 3 == 0:
        word = "Fizz"
    elif n % 5 == 0:
        word = "Buzz"
    else:
        word = str(n)
    print(word, end=" ")
    if n % 5 == 0:
        print()
