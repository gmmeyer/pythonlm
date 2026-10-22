fizz = 0
buzz = 0
both = 0
for n in range(1, 31):
    if n % 15 == 0:
        both += 1
    elif n % 3 == 0:
        fizz += 1
    elif n % 5 == 0:
        buzz += 1
print(f"Fizz: {fizz}, Buzz: {buzz}, FizzBuzz: {both}")
plain = 30 - fizz - buzz - both
print(f"Plain numbers: {plain}")
