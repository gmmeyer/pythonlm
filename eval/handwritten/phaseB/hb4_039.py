# A long night lit by candles. There are 3 candles in the box, each 11
# tall, burning 3 per hour. A burnt-out candle leaves a stub, and two stubs
# can be melted into a smaller candle of height 8. Burn until nothing is left.
box = 3
stubs = 0
height = 0
hours = 0
lit = False
print("candle night")
while True:
    if not lit:
        if box > 0:
            box -= 1
            height = 11
            lit = True
            print("light a new candle")
        elif stubs >= 2:
            stubs -= 2
            height = 8
            lit = True
            print("melt two stubs")
        else:
            break
    hours += 1
    height -= 3
    if height <= 0:
        lit = False
        stubs += 1
        print(hours)
print("hours of light")
print(hours)
print(stubs)
