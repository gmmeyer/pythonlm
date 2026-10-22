# first flip number where three heads in a row appear
x = 9
streak = 0
n = 0
while streak < 3 and n < 100:
    x = (x * 5 + 3) % 16
    n += 1
    if x < 8:
        streak += 1
    else:
        streak = 0
print(n)
print(streak == 3)
