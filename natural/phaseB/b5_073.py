# roman numeral symbol count for 888, greedy
n = 888
symbols = 0
while n >= 500:
    n -= 500
    symbols += 1
while n >= 100:
    n -= 100
    symbols += 1
while n >= 50:
    n -= 50
    symbols += 1
while n >= 10:
    n -= 10
    symbols += 1
while n >= 5:
    n -= 5
    symbols += 1
while n >= 1:
    n -= 1
    symbols += 1
print(symbols)
