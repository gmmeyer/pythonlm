n = 38
roman = ""
while n >= 10:
    roman = roman + "X"
    n = n - 10
if n == 9:
    roman = roman + "IX"
    n = 0
if n >= 5:
    roman = roman + "V"
    n = n - 5
if n == 4:
    roman = roman + "IV"
    n = 0
roman = roman + "I" * n
print("38 is", roman)
