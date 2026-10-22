# smallest number of days for stock to run out
stock = 100
day = 0
use = 5
while stock > 0:
    day += 1
    stock -= use
    use += 2
print(day)
print(stock)
