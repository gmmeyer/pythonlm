# first number past 50 with digit sum 12
n = 51
while n // 10 + n % 10 != 12:
    n += 1
print(n)
