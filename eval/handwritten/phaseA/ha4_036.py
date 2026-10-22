# Mixing paint for a mural, in milliliters. Each tin holds 750.
# Green is 3 parts yellow to 2 parts blue, orange is equal parts
# red and yellow, and purple is 1 part red to 3 parts blue.
# The total mixed is counted in units of 10 ml.

yellow = 750
blue = 750
red = 500
mixed = 0

print("Mix 400 green")
amount = 400
part = amount // 5
yellow -= part * 3
blue -= part * 2
mixed += amount // 10
print(yellow)
print(blue)

print("Mix 250 orange")
amount = 250
part = amount // 2
red -= part
yellow -= part
mixed += amount // 10
print(red)
print(yellow)

print("Mix 360 purple")
amount = 360
part = amount // 4
red -= part
blue -= part * 3
mixed += amount // 10
print(red)
print(blue)

print("Half a tin of yellow arrives")
yellow += 750 // 2
print(yellow)

print("Use up the blue on green")
# blue runs out first: 2 parts of blue per batch
part = blue // 2
yellow -= part * 3
blue -= part * 2
mixed += part * 5 // 10
print(part * 5)
print(yellow)
print(blue)

print("--- studio ---")
print(mixed)
print(yellow + blue + red)
