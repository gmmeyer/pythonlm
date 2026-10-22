digits = "0123456789abcdef"
n = 254
out = ""
while n > 0:
    out = digits[n % 16] + out
    n = n // 16
print("254 in hex:", out)
n = 171
out = ""
while n > 0:
    out = digits[n % 16] + out
    n = n // 16
print("171 in hex:", out)
