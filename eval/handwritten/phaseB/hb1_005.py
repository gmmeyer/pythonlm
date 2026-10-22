cart = 45
while cart < 260:
    if cart >= 200:
        off = 30
    elif cart >= 100:
        off = 15
    elif cart >= 50:
        off = 5
    else:
        off = 0
    print(cart - off)
    cart += 55
