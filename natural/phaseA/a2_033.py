# rotate the digits of 123 to the left, three times
n = 123
rotated = n % 100 * 10 + n // 100
print(rotated)
rotated = rotated % 100 * 10 + rotated // 100
print(rotated)
rotated = rotated % 100 * 10 + rotated // 100
print(rotated)
