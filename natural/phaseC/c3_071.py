n = 987
total = 0
digits = len(str(n))
while n > 0:
    total += n % 10
    n = n // 10
print("Digit sum is", total, "over", digits, "digits")
