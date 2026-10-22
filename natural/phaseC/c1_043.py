# roman numerals
num = 87
rest = num
roman = ""
while rest >= 50:
    roman = roman + "L"
    rest -= 50
if rest >= 40:
    roman = roman + "XL"
    rest -= 40
while rest >= 10:
    roman = roman + "X"
    rest -= 10
if rest == 9:
    roman = roman + "IX"
    rest = 0
if rest >= 5:
    roman = roman + "V"
    rest -= 5
if rest == 4:
    roman = roman + "IV"
    rest = 0
while rest > 0:
    roman = roman + "I"
    rest -= 1
print(num, "=", roman)
