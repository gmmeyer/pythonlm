# reverse a 3 digit number without strings
number = 357
a = number // 100
b = number // 10 % 10
c = number % 10
backwards = c * 100 + b * 10 + a
print("original:")
print(number)
print("reversed:")
print(backwards)
