# postage for letters of 10..60 grams, step 10
for grams in range(10, 61, 10):
    if grams <= 20:
        stamp = 1
    elif grams <= 50:
        stamp = 2
    else:
        stamp = 3
    print(stamp)
