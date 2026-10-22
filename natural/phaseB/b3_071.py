# count down by 5 and flag when it goes negative
n = 20
while n > -15:
    n -= 5
    if n < 0:
        print("below zero")
    print(n)
