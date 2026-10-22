# the decimal number 110 is meant as binary; convert it
digits = 110
value = 0
place = 1
while digits > 0:
    if digits % 10 == 1:
        value += place
    place *= 2
    digits //= 10
print(value)
