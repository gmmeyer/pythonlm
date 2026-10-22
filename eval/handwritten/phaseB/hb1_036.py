# what to wear, Celsius -> Fahrenheit
for c in range(-15, 41, 11):
    f = c * 9 // 5 + 32
    print(f)
    if f <= 32:
        print("freezing")
    elif f < 60:
        print("jacket")
    elif f < 85:
        print("t-shirt")
    else:
        print("stay inside")
