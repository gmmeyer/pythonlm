n = 49
roman = ""
while n >= 10:
    roman += "X"
    n -= 10
if n >= 9:
    roman += "IX"
    n -= 9
while n >= 5:
    roman += "V"
    n -= 5
if n == 4:
    roman += "IV"
    n -= 4
while n > 0:
    roman += "I"
    n -= 1
print("49 =", roman)
