# collect the digits of a number from the right
n = 904
digits = ""
while n > 0:
    digits = digits + str(n % 10)
    n = n // 10
print("digits reversed:", digits)
