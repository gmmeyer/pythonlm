# FizzBuzz with different divisors, up to 20
for i in range(1, 21):
    if i % 4 == 0:
        if i % 5 == 0:
            print("FizzBuzz")
        else:
            print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    elif i % 7 == 0:
        print("Bang")
    else:
        print(i)
